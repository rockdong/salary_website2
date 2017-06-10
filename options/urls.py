# _*_ coding:utf-8 _*_
__author__ = 'caidong'
__date__ = '2017/3/19 21:12'


from django.conf.urls import url

from options.views import IndexView, AddUserView, UserListView, \
    UserDeleteView, SalaryView, SetPasswordView, SalaryDetailView,\
    SalaryDetailInfoView, SalaryCollectView, DataUpdateView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^add_user/', AddUserView.as_view(), name='add_user'),
    url(r'^user_list/', UserListView.as_view(), name='user_list'),
    url(r'^user_delete/(?P<id>.*)/', UserDeleteView.as_view(), name='user_delete'),
    url(r'^salary/(?P<start_date>.*)/(?P<end_date>.*)/', SalaryView.as_view(), name='salary'),
    url(r'^salary_detail/(?P<start_date>.*)/(?P<cur_date>.*)/(?P<end_date>.*)/', SalaryDetailView.as_view(), name='salary_detail'),
    url(r'^salary_detail_info/', SalaryDetailInfoView.as_view(), name='salary_detail_info'),
    url(r'^salary_collect/', SalaryCollectView.as_view(), name='salary_collect'),
    url(r'^set_password/(?P<id>.*)/', SetPasswordView.as_view(), name='set_password'),
    url(r'^add_data/', DataUpdateView.as_view(), name='add_data'),
]
