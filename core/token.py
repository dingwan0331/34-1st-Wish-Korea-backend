import jwt

from datetime import datetime, timedelta

from django.core.cache import cache
from django.http       import JsonResponse

from my_settings import SECRET_KEY, REFRESH_TOKEN_SECRET_KEY, ACCESS_TOKEN_ALGORITHM, REFRESH_TOKEN_ALGORITHM

class Token:
    def __init__(self, type):
        self.type    = type
        self.EXPIRES = {
            'access_token': datetime.utcnow() + timedelta(seconds = 1), 
            'refresh_token': datetime.utcnow() + timedelta(hours = 8)
            }
        self.ALGORITHMS  = {'access_token': ACCESS_TOKEN_ALGORITHM , 'refresh_token': REFRESH_TOKEN_ALGORITHM}
        self.SECRET_KEYS = {'access_token': SECRET_KEY , 'refresh_token':REFRESH_TOKEN_SECRET_KEY}
        
    def sign_token(self, user_id):
        payload    = {"id": user_id, "exp": self.EXPIRES[self.type] }
        ALGORITHM  = self.ALGORITHMS[self.type]
        SECRET_KEY = self.SECRET_KEYS[self.type]

        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

        return token

    def sign_token_again(self, access_token):
        try:
            refresh_token            = cache.get(access_token)
            REFRESH_TOKEN_ALGORITHM  = self.ALGORITHMS['refresh_token']
            REFRESH_TOKEN_SECRET_KEY = self.SECRET_KEYS['refresh_token']
            user_id                  = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET_KEY, REFRESH_TOKEN_ALGORITHM)['id']
            access_token             = self.sign_token(user_id)

            return access_token

        except jwt.exceptions.ExpiredSignatureError:
            raise Exception()