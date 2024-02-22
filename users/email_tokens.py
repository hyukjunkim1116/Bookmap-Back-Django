from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return user.id + timestamp


account_activation_token = AccountActivationToken()
