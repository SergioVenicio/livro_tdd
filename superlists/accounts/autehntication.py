import sys
from . import models


class PasswordlessAuthenticationBackend:
    def authenticate(self, uid):
        print('uid', uid, file=sys.stderr)
        if not models.Token.objects.filter(uid=uid).exists():
            print('No token found', file=sys.stderr)
            return None

        token = models.Token.objects.get(uid=uid)
        print('got token', token, file=sys.stderr)
        try:
            user = models.ListUser.objects.get(email=token.email)
            print('got user', user, file=sys.stderr)
            return user
        except models.ListUser.DoesNotExist:
            print('new User', file=sys.stderr)
            return models.ListUser.objects.create(email=token.email)


    def get_user(self, email):
        return models.ListUser.objects.get(email=email)
