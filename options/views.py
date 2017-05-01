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
from salary.models import *

from user_profile.forms import LoginForm, RegisterForm


# 获取 所有对像
def getSalary(cur_user, cur_date):
    try:
        pyepa = PreYearEndPerformanceAppraisa.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        pyepa = None
    try:
        gpa = GovPerformanceAppraisa.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        gpa = None
    try:
        sba = SpecialBenefitAward.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        sba = None
    try:
        cda = CadreDutyAward.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        cda = None
    try:
        rs = ReallySalary.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        rs = None
    try:
        f = Food.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        f = None
    return pyepa, gpa, sba, cda, rs, f


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
查看薪水
'''
class SalaryView(View):
    def get(self, request, start_date, end_date):
        try:
            # 当前用户
            cur_user = request.user
            if start_date == "":
                startDate = datetime.datetime.now()
                endDate = startDate
            else:
                startDate = datetime.datetime.strptime(start_date, '%Y-%m')
                endDate = datetime.datetime.strptime(end_date, '%Y-%m')

            datas = []
            date = startDate
            last = startDate
            datas.append(self.getData(cur_user, date))
            while date < endDate:
                date = date + datetime.timedelta(weeks=4)
                date = datetime.datetime(date.year, date.month, 1)
                if date == last:
                    date = date + datetime.timedelta(weeks=1)
                else:
                    datas.append(self.getData(cur_user, date))
                last = date

            return render(request, 'salary.html', {"datas": datas, "start_date": startDate, "end_date": endDate})
        except Exception as e:
            return render(request, 'salary.html', {})

    # 根据日期获取集合
    def getData(self, cur_user, cur_date):
        data = {}
        try:
            pyepa, gpa, sba, cda, rs, f = getSalary(cur_user, cur_date)

            # 日期
            data['date'] = cur_date
            # 应发合计
            data['salary'] = self.getSalaryCount(pyepa, gpa, sba, cda, rs, f)
            # 应扣合计
            data['discount'] = self.getSalaryDiscount(pyepa, gpa, sba, cda, rs, f)
            # 实发合计
            data['really_salary'] = self.getSalaryReallyCount(pyepa, gpa, sba, cda, rs, f)
            return data
        except Exception as e:
            # 日期
            data['date'] = cur_date
            # 应发合计
            data['salary'] = "无数据"
            # 应扣合计
            data['discount'] = "无数据"
            # 实发合计
            data['really_salary'] = "无数据"
            return data

    # 应发
    def getSalaryCount(self, pyepa, gpa, sba, cda, rs, f):
        try:
            return pyepa.amount + gpa.amount + sba.amount + cda.standard + \
                   rs.post_wage + rs.level_wage + rs.area_allowance + rs.base_allowance + f.amount
        except Exception as e:
            return "无数据"

    # 应扣除
    def getSalaryDiscount(self, pyepa, gpa, sba, cda, rs, f):
        try:
            return gpa.tax + cda.tax + rs.urance_benefit + \
                   rs.housing_fund + rs.housing_fund2 + rs.tax + \
                   rs.rent + rs.utilities + rs.other
        except Exception as e:
            return "无数据"

    # 实发
    def getSalaryReallyCount(self, pyepa, gpa, sba, cda, rs, f):
        try:
            return pyepa.amount + gpa.amount - gpa.tax + sba.amount + cda.standard - cda.tax + \
                   rs.post_wage + rs.level_wage + rs.area_allowance + rs.base_allowance - \
                   rs.urance_benefit - rs.housing_fund - rs.housing_fund2 - rs.tax - \
                   rs.rent - rs.utilities - rs.other + f.amount
        except Exception as e:
            return "无数据"


'''
某月工资详情
'''
class SalaryDetailView(View):
    def get(self, request, start_date, cur_date, end_date):
        cur_user = request.user
        datas = self.getDatas(cur_user, datetime.datetime.strptime(cur_date, "%Y-%m"))

        return render(request, 'salary_detail.html', {'datas': datas, 'cur_date': cur_date, \
                                                      'start_date': start_date, 'end_date': end_date})

    def getDatas(self, cur_user, cur_date):
        datas = []
        try:
            pyepa, gpa, sba, cda, rs, f = getSalary(cur_user, cur_date)
            if pyepa is not None:
                data = {}
                data['type'] = 'pyepa'
                # 内容
                data['title'] = pyepa.title
                # 应发合计
                data['salary'] = pyepa.standard
                # 应扣合计
                data['discount'] = pyepa.tax
                # 实发合计
                data['really_salary'] = pyepa.amount
                datas.append(data)
            if gpa is not None:
                data = {}
                data['type'] = 'gpa'
                # 内容
                data['title'] = gpa.title
                # 应发合计
                data['salary'] = gpa.standard
                # 应扣合计
                data['discount'] = gpa.tax
                # 实发合计
                data['really_salary'] = gpa.amount
                datas.append(data)
            if sba is not None:
                data = {}
                data['type'] = 'sba'
                # 内容
                data['title'] = sba.title
                # 应发合计
                data['salary'] = sba.standard
                # 应扣合计
                data['discount'] = sba.tax
                # 实发合计
                data['really_salary'] = sba.amount
                datas.append(data)
            if cda is not None:
                data = {}
                data['type'] = 'cda'
                # 内容
                data['title'] = cda.title
                # 应发合计
                data['salary'] = cda.standard
                # 应扣合计
                data['discount'] = cda.tax
                # 实发合计
                data['really_salary'] = cda.standard - cda.tax
                datas.append(data)
            if rs is not None:
                data = {}
                data['type'] = 'rs'
                # 内容
                data['title'] = rs.title
                # 应发合计
                data['salary'] = rs.post_wage + rs.level_wage + rs.area_allowance + rs.base_allowance
                # 应扣合计
                data['discount'] = rs.housing_fund + rs.housing_fund2 + rs.tax + \
                                   rs.rent + rs.utilities + rs.other
                # 实发合计
                data['really_salary'] = rs.post_wage + rs.level_wage + rs.area_allowance + rs.base_allowance - \
                                        rs.urance_benefit - rs.housing_fund - rs.housing_fund2 - rs.tax - \
                                        rs.rent - rs.utilities - rs.other
                datas.append(data)
            if f is not None:
                data = {}
                data['type'] = 'f'
                # 内容
                data['title'] = f.title
                # 应发合计
                data['salary'] = f.standard
                # 应扣合计
                data['discount'] = f.tax
                # 实发合计
                data['really_salary'] = f.amount
                datas.append(data)
            return datas
        except Exception as e:
            return None


class SalaryDetailInfoView(View):
    def post(self, request):
        try:
            cur_user = request.user
            type = request.POST.get('type', None)
            cur_date = datetime.datetime.strptime(request.POST.get('date', None), '%Y-%m')
            pyepa, gpa, sba, cda, rs, f = getSalary(cur_user, cur_date)
            data = {}
            if "pyepa" == type:
                data['title'] = pyepa.title
                data['text'] = "标准: " + str(pyepa.standard) + "</br>数量: " + str(pyepa.index) + "</br>金额: "\
                               + str(pyepa.amount) \
                               + "</br>其它补: " + str(pyepa.other)  + "</br>扣所得税: " + str(pyepa.tax) \
                               + "</br></br>实发合计: " + str(pyepa.amount)
            elif "gpa" == type:
                data['title'] = gpa.title
                data['text'] = "标准: " + str(gpa.standard) + "</br>系数: " + str(gpa.ratio) + "</br>金额: " + str(gpa.amount) \
                               + "</br>扣所得税: " + str(gpa.tax) + "</br>扣其它: " + str(gpa.other)\
                               + "</br></br>实发合计: " + str(gpa.amount)
            elif "sba" == type:
                data['title'] = sba.title
                data['text'] = "标准: " + str(sba.standard) + "</br>数量: " + str(sba.index) + "</br>金额: " + str(sba.amount) \
                               + "</br>扣其它: " + str(sba.other) + "</br>扣所得税: " + str(sba.tax) \
                               + "</br></br>实发合计: " + str(sba.amount)
            elif "cda" == type:
                data['title'] = cda.title
                data['text'] = "职务津贴标准: " + str(cda.standard) + "</br>数量: " + str(cda.index) \
                               + "</br>扣其它: " + str(cda.other) + "</br>扣所得税: " + str(cda.tax) \
                               + "</br></br>实发合计: " + str(cda.standard - cda.tax)
            elif "rs" == type:
                data['title'] = rs.title
                data['text'] = "岗位工资: " + str(rs.post_wage) + "</br>薪级工资: " + str(rs.level_wage)\
                               + "</br>特区津贴: " + str(rs.area_allowance) \
                               + "</br>基础津贴: " + str(rs.base_allowance) + "</br>特殊岗位津贴: " \
                               + str(rs.special_post_allowance) \
                               + "</br>紧缺岗位: " + str(rs.shortage_post) + "</br>护龄: " + str(rs.nursing_age) \
                               + "</br>保险金: " + str(rs.urance_benefit) + "</br>住房公积金: " + str(rs.housing_fund) \
                               + "</br>住房公积金2: " + str(rs.housing_fund2) + "</br>扣所得税: " + str(rs.tax) \
                               + "</br>扣房租: " + str(rs.rent) + "</br>扣水电: " + str(rs.utilities) \
                               + "</br>扣其它: " + str(rs.other) + "</br></br>实发合计: " + str(rs.post_wage + rs.level_wage + rs.area_allowance + rs.base_allowance - \
                                            rs.urance_benefit - rs.housing_fund - rs.housing_fund2 - rs.tax - \
                                            rs.rent - rs.utilities - rs.other)
            elif "f" == type:
                data['title'] = f.title
                data['text'] = "标准: " + str(f.standard) + "</br>数量: " + str(f.index) + "</br>金额: " + str(f.amount) \
                               + "</br>扣所得税: " + str(f.tax) + "</br></br>实发合计: " + str(f.amount)
            else:
                return HttpResponse(json.dumps({"status": "fail", "msg": "查询错误!"}), content_type="application/json")

            return HttpResponse(json.dumps({"status": "success", "data": data}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"status": "fail", "msg": "查询错误!"}), content_type="application/json")


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

