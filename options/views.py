# _*_ coding:utf-8 _*_

from django.shortcuts import render
from django.core.serializers import serialize

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
import json
import datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password

from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from user_profile.models import UserProfile

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