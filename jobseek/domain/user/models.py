import uuid
from collections import OrderedDict
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from jobseek.common.behaviors import Timestampable

from .manager import UserProfileManager

logger = logging.getLogger('jobseek.user')


class UserProfile(Timestampable, models.Model):
    user_profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                                       help_text='user_profile_id')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=100, null=True)
    tel_num = models.CharField(max_length=20, null=True)
    masked_name = models.CharField(max_length=100, null=True)
    masked_tel_num = models.CharField(max_length=20, null=True)
    birthday = models.DateField(null=True)
    sex = models.IntegerField(null=True)

    objects = UserProfileManager()

    class Meta:
        db_table = 'user_profile'

    def get_masked_name(self, name):
        masked_name = name[0]
        if len(name) == 2:
            return masked_name + '*'
        else:
            for i in range(len(name) - 2):
                masked_name += '*'
            return masked_name + name[-1]

    def get_masked_tel_num(self, tel_num):
        return tel_num[:3] + '****' + tel_num[-4:]

    def __str__(self):
        return f'{self.masked_name}|{self.user_profile_id}'

