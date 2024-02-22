from PyKakao import Message
from django.conf import settings
import requests
import json


def getFriendsList(access_token):
    header = {"Authorization": "Bearer " + access_token}
    url = "https://kapi.kakao.com/v1/api/talk/friends"  # 친구 정보 요청

    result = json.loads(requests.get(url, headers=header).text)

    friends_list = result.get("elements")
    friends_id = []

    for friend in friends_list:
        friends_id.append(str(friend.get("uuid")))


# 나에게 보내기 , 다른 사람에게 보내기는 api사용 요청 해야함
def kakao_message(access_token, user_data):
    API = Message(service_key=settings.KAKAO_REST_API_KEY)
    API.set_access_token(access_token)
    # UUID 목록
    # receiver_uuids = [
    #     "수신자 UUID",
    # ]

    # 파라미터
    kakao_account = user_data.get("kakao_account")
    profile = kakao_account.get("profile")
    # 메시지 유형 - 피드
    message_type = "feed"
    # 파라미터
    content = {
        "title": "유저가 로그인 했습니다.",
        "description": f'{ profile.get("nickname")}님이 로그인 했습니다.\n 로그인 일시 : {user_data.get("connected_at")}',
        "image_url": f'{profile.get("profile_image_url")}',
        "image_width": 640,
        "image_height": 640,
        "link": {
            "web_url": "http://www.daum.net",
            "mobile_web_url": "http://m.daum.net",
            "android_execution_params": "contentId=100",
            "ios_execution_params": "contentId=100",
        },
    }

    buttons = [
        {
            "title": "홈페이지로 이동",
            "link": {
                "web_url": "http://www.daum.net",
                "mobile_web_url": "http://m.daum.net",
            },
        }
    ]

    API.send_message_to_me(message_type=message_type, content=content, buttons=buttons)
