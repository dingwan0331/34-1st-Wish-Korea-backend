from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel):
    username      = models.CharField(max_length = 50, unique = True)
    password      = models.CharField(max_length = 200)
    email         = models.CharField(max_length = 100, unique = True)
    phone_number  = models.CharField(max_length = 50, unique = True)
    first_name    = models.CharField(max_length = 50)
    last_name     = models.CharField(max_length = 50)
    address       = models.CharField(max_length = 200, default = '')
    nick_name     = models.CharField(max_length = 50, default = '')
    refresh_token = models.CharField(max_length = 150, null = True)

    class Meta:
        db_table = 'users'