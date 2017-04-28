# _*_ coding:utf-8 _*_

import os

from django.shortcuts import render
from django.core.serializers import serialize
import xlrd

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
import json
import datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password

from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from user_profile.models import UserProfile
from salary.models import Salary

from user_profile.forms import LoginForm, RegisterForm


'''
用户登陆
'''
class LoginView(View):
    def get(self, request):
        try:
            has_superuser = UserProfile.objects.filter(is_superuser=True).exists()
            return render(request, 'login.html', {"has_superuser": has_superuser})
        except Exception as e:
            return render(request, 'login.html', {"has_superuser": False})

    def post(self, request):
        try:
            has_superuser = UserProfile.objects.filter(is_superuser=True).exists()

            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('index/')
                else:
                    return render(request, 'login.html', {"has_superuser": has_superuser})
            else:
                return render(request, 'login.html', {"has_superuser": has_superuser, "login_form": login_form})
        except Exception as e:
            return HttpResponseRedirect('/')


'''
用户退出
'''
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


'''
用户注册
'''
class RegisterView(View):
    def get(self, request):
        return render(request, 'regist.html', {})

    def post(self, request):
        try:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                username = request.POST.get('username', '')
                user = UserProfile.objects.filter(username=username).exists()
                if not user :
                    user = UserProfile()
                    user.username = username
                    user.password = make_password(request.POST.get('password', ''))
                    user.name = request.POST.get('name', '')
                    user.is_superuser = True
                    user.is_active = True
                    user.is_staff = True
                    user.save()
                    return HttpResponseRedirect('/')
                else:
                    return render(request, 'regist.html', {"msg": "用户已经存在"})
            else:
                return render(request, 'regist.html', {"register_form": register_form})
        except Exception as e:
            return render(request, 'regist.html', {})


'''
主页
'''
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html', {})


'''
添加人员
'''
class AddUserView(View):
    def get(self, request):
        return render(request, 'add_staffs.html', {})

    def post(self, request):
        try:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                username = request.POST.get('username', '')
                user = UserProfile.objects.filter(username=username).exists()
                if not user:
                    user = UserProfile()
                    user.username = username
                    user.password = make_password(request.POST.get('password', ''))
                    user.name = request.POST.get('name', '')
                    user.is_superuser = False
                    user.is_active = True
                    user.is_staff = True
                    user.save()
                    return HttpResponse(json.dumps({"status": "success", "msg": "人员添加成功!"}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"status": "fail", "msg": "所添加的用户已经存在!"}), content_type="application/json")
            else:
                return render(request, 'add_staffs.html', {"register_form": register_form})
        except Exception as e:
            return HttpResponse(json.dumps({"status": "fail", "msg": "执行错误!"}), content_type="application/json")


'''
人员查看
'''
class UserListView(View):
    def get(self, request):
        user_list = UserProfile.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(user_list, 5, request=request)
        users = p.page(page)
        return render(request, 'staffs.html', {"users": users})


'''
人员删除
'''
class UserDeleteView(View):
    def post(self, request, id):
        try:
            user = UserProfile.objects.get(id=id)
            user.delete()
            return HttpResponse(json.dumps({"status": "success", "msg": "用户删除成功!"}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"status": "fail", "msg": "用户删除失败!"}), content_type="application/json")


'''
添加数据
'''
class DataAddView(View):
    def get(self, request):
        return render(request, 'add_data.html', {})

    def post(self, request):
        try:
            file = request.FILES.get('file', '')

            # 文件名判断
            filename = file.name
            pathname = filename.split('.')[-1]

            if pathname != u"xls" and pathname != u"xlsx" :
                return HttpResponse(json.dumps({"status": "fail", "msg": "文件不是 Excel 文件!"}), content_type="application/json")


            baseDir = os.path.dirname(os.path.abspath(__name__))
            jpgdir = os.path.join(baseDir, 'static')

            filename = os.path.join(jpgdir, file.name)
            fobj = open(filename, 'wb')
            for chrunk in file.chunks():
                fobj.write(chrunk)
            fobj.close()



            excelFile = xlrd.open_workbook(filename)

            table = excelFile.sheets()[0]

            print table.nrows
            print table.ncols

            for i in range(2, table.nrows):
                print table.cell_value(i, 0)
                print xlrd.xldate.xldate_as_datetime(table.cell_value(i, 1), 1)
                print table.cell_value(i, 2)

                salary = Salary()
                user = UserProfile.objects.get(username=table.cell_value(i, 0))
                salary.user = user
                salary.date = xlrd.xldate.xldate_as_datetime(table.cell_value(i, 1), 1)
                salary.salary = table.cell_value(i, 2)
                salary.save()

            # 删除文件
            os.remove(filename)

            return HttpResponse(json.dumps({"status": "success", "msg": "数据添加成功!"}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"status": "fail", "msg": "操作错误!"}), content_type="application/json")


'''
查看薪水
'''
class SalaryView(View):
    def get(self, request, name):
        all_salary = Salary.objects.filter(user__name=name)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_salary, 5, request=request)
        salarys = p.page(page)
        return render(request, 'salary.html', {"salarys": salarys})


'''
修改密码
'''
class SetPasswordView(View):
    def get(self, request):
        return render(request, 'set_password.html', {})

    def post(self, request):
        return HttpResponse(json.dumps({"status": "success", "msg": "修改密码成功!"}), content_type="application/json")


'''
查看报表
'''

