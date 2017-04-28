# _*_ coding:utf-8 _*_
__author__ = 'caidong'
__date__ = '2017/3/19 21:12'


from django.conf.urls import url

from options.views import IndexView, AddUserView, UserListView, UserDeleteView, DataAddView, SalaryView, SetPasswordView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^add_user/', AddUserView.as_view(), name='add_user'),
    url(r'^user_list/', UserListView.as_view(), name='user_list'),
    url(r'^user_delete/(?P<id>.*)/', UserDeleteView.as_view(), name='user_delete'),
    url(r'^data_add/', DataAddView.as_view(), name='data_add'),
    url(r'^salary/(?P<name>.*)/', SalaryView.as_view(), name='salary'),
    url(r'^set_password/', SetPasswordView.as_view(), name='set_password'),
]
