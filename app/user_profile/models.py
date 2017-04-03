# _*_ coding:utf-8 _*_

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    name = models.CharField(max_length=20, null=False, blank=False, verbose_name='姓名')

    class Meta:
        verbose_name = '成员'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name