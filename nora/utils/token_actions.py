import uuid
import secrets, hashlib
from datetime import timedelta

from django.shortcuts import get_object_or_404
from nora.models import UserToken
from django.utils import timezone


class TokenUser:
    def __init__(self, user=None, menu=None):
        self.user = user
        self.menu =menu

    def generate_token(self):
        token = uuid.uuid4().hex
        token_user = UserToken.objects.create(user_id=self.user, token_user=token, menu=self.menu)
        return token_user.token_user

    @staticmethod
    def validate_token(token, user_id):
        user_token = get_object_or_404(UserToken, token=token)
        if not user_token.user_id == user_id:
            return Exception('Token no valid')
        time_now = timezone.now()
        if user_token.datetime > (time_now - timedelta(hours=2)):
            return Exception('Token has expired')
        return True

