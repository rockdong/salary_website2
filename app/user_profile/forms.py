# _*_ coding:utf-8 _*_
__author__ = 'caidong'
__date__ = '2017/4/3 1:43'

from django import forms
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)