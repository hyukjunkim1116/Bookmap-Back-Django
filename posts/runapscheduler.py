# runapscheduler.py
import logging
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.conf import settings
from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from apscheduler.triggers.cron import CronTrigger
import boto3

logger = logging.getLogger(__name__)


def get_s3_client():
    # S3 클라이언트 생성 및 반환
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )


@util.close_old_connections
def delete_old_job_executions(max_age=1):

    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def delete_post_images():

    s3_client = get_s3_client()
    # 폴더 안의 객체 리스트업

    response = s3_client.list_objects(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix="posts/"
    )

    if response.get("Contents") is not None:

        for obj in response.get("Contents", []):
            s3_client.delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=obj["Key"]
            )


class Command(BaseCommand):

    def start(self, *args, **options):
        scheduler = BackgroundScheduler(
            timezone=settings.TIME_ZONE
        )  # BlockingScheduler를 사용할 수도 있습니다.
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            delete_post_images,
            trigger=CronTrigger(minute="*/59"),
            id="delete_post_images",  # id는 고유해야합니다.
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'delete_post_images'.")
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(minute="*/59"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
