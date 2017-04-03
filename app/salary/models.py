# _*_ coding:utf-8 _*_

from __future__ import unicode_literals

from django.db import models

from user_profile.models import UserProfile

# Create your models here.


class Salary(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='时间')
    salary = models.FloatField(verbose_name='工资')

    class Meta:
        verbose_name = '工资'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user.name + "|" + self.date + "|" + self.salary
