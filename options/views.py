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

from user_profile.forms import LoginForm


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


class RegisterView(View):
    def get(self, request):
        return render(request, 'regist.html', {})
