# _*_ coding:utf-8 _*_
__author__ = 'caidong'
__date__ = '2017/3/19 21:12'


from django.conf.urls import url

from options.views import IndexView, AddUserView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^add_user/', AddUserView.as_view(), name='add_user'),
]
