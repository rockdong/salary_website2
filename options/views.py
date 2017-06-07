# _*_ coding:utf-8 _*_

import os
import threading
import time
from salary_system.settings import FILE_ROOT

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
        m = Medical.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        m = Medical()
    try:
        th = TackHoliday.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        th = TackHoliday()
    try:
        h = Holiday.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        h = Holiday()
    try:
        sc = SingleChild.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        sc = SingleChild()
    try:
        pa = PerformanceAppraisa.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        pa = PerformanceAppraisa()
    try:
        ns = NonStaff.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        ns = NonStaff()
    try:
        a = Assess.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        a = Assess()
    try:
        p = Provide.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        p = Provide()
    try:
        b = Basic.objects.get(user=cur_user, date__year=cur_date.year, date__month=cur_date.month)
    except Exception as e:
        b = Basic()
    return m, th, h, sc, pa, ns, a, p, b


# 根据日期获取集合
def getData(cur_user, cur_date):
    data = {}
    try:
        m, th, h, sc, pa, ns, a, p, b = getSalary(cur_user, cur_date)

        if m.pk is not None or th.pk is not None or h.pk is not None or \
            sc.pk is not None or pa.pk is not None or ns.pk is not None or \
            a.pk is not None or p.pk is not None or b.pk is not None :
            # 日期
            data['date'] = cur_date
            # 应发合计
            data['salary'] = getSalaryCount(m, th, h, sc, pa, ns, a, p, b)
            # 应扣合计
            data['discount'] = getSalaryDiscount(m, th, h, sc, pa, ns, a, p, b)
            # 实发合计
            data['really_salary'] = data['salary'] - data['discount']
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
def getSalaryCount(m, th, h, sc, pa, ns, a, p, b):
    try:
        return m.salary + th.salary + sc.salary + pa.award + h.salary + ns.salary + ns.old + ns.house_fix + a.salary + p.salary + b.salary
    except Exception as e:
        return "无数据"

# 应扣除
def getSalaryDiscount(m, th, h, sc, pa, ns, a, p, b):
    try:
        return pa.tax + ns.house_p
    except Exception as e:
        return "无数据"

# # 实发
# def getSalaryReallyCount(m, th, sc, pa, ns, a, p, b):
#     try:
#         return pyepa.amount + gpa.amount - gpa.tax + sba.amount + cda.standard - cda.tax + \
#                rs.post_wage + rs.level_wage + rs.area_allowance + rs.base_allowance - \
#                rs.urance_benefit - rs.housing_fund - rs.housing_fund2 - rs.tax - \
#                rs.rent - rs.utilities - rs.other + f.amount
#     except Exception as e:
#         return "无数据"


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
                if not user:
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
            datas.append(getData(cur_user, date))
            while date < endDate:
                date = date + datetime.timedelta(weeks=4)
                date = datetime.datetime(date.year, date.month, 1)
                if date == last:
                    date = date + datetime.timedelta(weeks=1)
                else:
                    datas.append(getData(cur_user, date))
                last = date

            return render(request, 'salary.html', {"datas": datas, "start_date": startDate, "end_date": endDate})
        except Exception as e:
            return render(request, 'salary.html', {})




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
            m, th, h, sc, pa, ns, a, p, b = getSalary(cur_user, cur_date)
            if m.pk is not None:    #统筹医疗发放
                data = {}
                data['type'] = 'm'
                # 内容
                data['title'] = "统筹医疗发放"
                # 应发合计
                data['salary'] = m.salary
                # 应扣合计
                data['discount'] = 0.0
                # 实发合计
                data['really_salary'] = m.salary
                datas.append(data)
            if th.pk is not None:   #未休年休假工资报酬发放
                data = {}
                data['type'] = 'th'
                # 内容
                data['title'] = "未休年休假工资报酬发放"
                # 应发合计
                data['salary'] = th.salary
                # 应扣合计
                data['discount'] = 0.0
                # 实发合计
                data['really_salary'] = th.salary
                datas.append(data)
            if h.pk is not None:    #节日补贴
                data = {}
                data['type'] = 'h'
                # 内容
                data['title'] = h.holiday
                # 应发合计
                data['salary'] = h.salary
                # 应扣合计
                data['discount'] = 0.0
                # 实发合计
                data['really_salary'] = h.salary
                datas.append(data)
            if sc.pk is not None:   #独生子女优待费发放
                data = {}
                data['type'] = 'sc'
                # 内容
                data['title'] = "独生子女优待费发放"
                # 应发合计
                data['salary'] = sc.salary
                # 应扣合计
                data['discount'] = 0.0
                # 实发合计
                data['really_salary'] = sc.salary
                datas.append(data)
            if pa.pk is not None:   #绩效考核奖发放
                data = {}
                data['type'] = 'pa'
                # 内容
                data['title'] = "绩效考核奖发放"
                # 应发合计
                data['salary'] = pa.salary + pa.award
                # 应扣合计
                data['discount'] = pa.tax
                # 实发合计
                data['really_salary'] = pa.salary + pa.award - pa.tax
                datas.append(data)
            if ns.pk is not None:   #非统发人员工资及统发人员津贴发放
                data = {}
                data['type'] = 'ns'
                # 内容
                data['title'] = "非统发人员工资及统发人员津贴发放"
                # 应发合计
                data['salary'] = ns.salary + ns.house_fix + ns.medical + ns.old
                # 应扣合计
                data['discount'] = ns.house_p
                # 实发合计
                data['really_salary'] = ns.salary + ns.house_fix + ns.medical + ns.old - ns.house_p
                datas.append(data)
            if a.pk is not None:   #补发考核奖发放
                data = {}
                data['type'] = 'a'
                # 内容
                data['title'] = "补发考核奖发放"
                # 应发合计
                data['salary'] = a.salary
                # 应扣合计
                data['discount'] = 0.0
                # 实发合计
                data['really_salary'] = a.salary
                datas.append(data)
            if p.pk is not None:   #养老保险临时补贴
                data = {}
                data['type'] = 'p'
                # 内容
                data['title'] = "养老保险临时补贴"
                # 应发合计
                data['salary'] = p.salary
                # 应扣合计
                data['discount'] = 0.0
                # 实发合计
                data['really_salary'] = p.salary
                datas.append(data)
            if b.pk is not None:   #基层补贴
                data = {}
                data['type'] = 'b'
                # 内容
                data['title'] = "基层补贴"
                # 应发合计
                data['salary'] = b.salary
                # 应扣合计
                data['discount'] = 0.0
                # 实发合计
                data['really_salary'] = b.salary
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
            m, th, h, sc, pa, ns, a, p, b = getSalary(cur_user, cur_date)
            data = {}
            if "m" == type:
                data['title'] = "统筹医疗发放"
                data['text'] = "应发金额:" + str(m.salary)
            elif "th" == type:
                data['title'] = "未休年休假工资报酬发放"
                data['text'] = "应发金额:" + str(th.salary)
            elif "h" == type:
                data['title'] = m.title
                data['text'] = "节日补贴:" + str(m.salary)
            elif "sc" == type:
                data['title'] = "独生子女优待费发放"
                data['text'] = "应发金额:" + str(sc.salary)
            elif "pa" == type:
                data['title'] = "绩效考核奖发放"
                data['text'] = "2.5倍考核奖:" + str(pa.award) + "</br>所得税:" + str(pa.tax) + "</br>实发合计:" + str(pa.salary)
            elif "ns" == type:
                data['title'] = "非统发人员工资及统发人员津贴发放"
                data['text'] = "年金:" + str(ns.salary) + "</br>个人统筹医疗:" + str(ns.medical) \
                               + "</br>养老补差:" + str(ns.old) + "</br>住房公积金（个人）:" + str(ns.house_p) \
                               + "</br>住房公积金（单位）:" + str(ns.house_o) + "</br>房改住房补贴:" + str(ns.house_fix)
            elif "a" == type:
                data['title'] = "补发考核奖发放"
                data['text'] = "年度考核奖:" + str(a.salary)
            elif "p" == type:
                data['title'] = "养老保险临时补贴"
                data['text'] = "养老保险临时补贴:" + str(p.salary)
            elif "b" == type:
                data['title'] = "基层补贴"
                data['text'] = "基层补贴:" + str(b.salary)
            else:
                return HttpResponse(json.dumps({"status": "fail", "msg": "查询错误!"}), content_type="application/json")

            return HttpResponse(json.dumps({"status": "success", "data": data}), content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"status": "fail", "msg": "查询错误!"}), content_type="application/json")


'''
查看报表
'''
class SalaryCollectView(View):
    def get(self, request):
        return render(request, 'salary_collect.html', {})

    def post(self, request):
        try:
            cur_user = request.user

            start_date = datetime.datetime.strptime(request.POST.get('start_date', None), '%Y-%m')
            end_date = datetime.datetime.strptime(request.POST.get('end_date', None), '%Y-%m')

            temp_data = {}
            date = start_date
            last = end_date

            salary = 0.0
            # 应扣合计
            discount = 0.0
            # 实发合计
            really_salary = 0.0

            temp_data = getData(cur_user, date)

            salary += temp_data['salary']
            discount += temp_data['discount']
            really_salary += temp_data['really_salary']

            while date < end_date:
                date = date + datetime.timedelta(weeks=4)
                date = datetime.datetime(date.year, date.month, 1)
                if date == last:
                    date = date + datetime.timedelta(weeks=1)
                else:
                    temp_data = getData(cur_user, date)
                    salary += temp_data['salary']
                    discount += temp_data['discount']
                    really_salary += temp_data['really_salary']
                last = date

            return HttpResponse(json.dumps({"status": "success", "start_date": start_date.strftime('%Y-%m'), "end_date": end_date.strftime('%Y-%m'), \
                                            "salary": salary, "discount": discount, "really_salary": really_salary \
                                            }), content_type="application/json")
        except Exception as e:
            return render(request, 'salary_collect.html', {})


'''
修改密码
'''
class SetPasswordView(View):
    def get(self, request):
        return render(request, 'set_password.html', {})

    def post(self, request):
        return HttpResponse(json.dumps({"status": "success", "msg": "修改密码成功!"}), content_type="application/json")



'''
上传文件
'''
class DataUpdateView(View):
    def get(self, request):
        return render(request, 'add_data.html', {})

    def post(self, request):
        # 家属统筹医疗费发放
        self.medicalFile(request)
        # 未休年休假工资报酬发放
        self.vacationFile(request)
        # 独生子女费
        self.onlyFile(request)
        # 绩效考核奖发放
        self.performanceAppraisaFile(request)
        # 非统发人员工资及统发人员津贴发放
        self.nonStaffFile(request)
        # 过节费
        self.holidayFile(request)
        # 基层补贴
        self.basicFile(request)
        # 养老保险临时补贴
        self.oldFile(request)
        # 补发考核奖
        self.performanceAppraisaFixFile(request)

        return HttpResponse(json.dumps({"status": "success", "msg": "文件读取完毕!"}), content_type="application/json")

    # 判断是否为数字
    def isNum(self, value):
        try:
            int(value)
            return True
        except Exception as e:
            return False

    # 家属统筹医疗费发放
    def medicalFile(self, request):
        # 保存文件
        file = request.FILES.get('medical', None)
        if file:
            fd = open(os.path.join(FILE_ROOT, file.name), 'wb+')
            for chunk in file.chunks():
                fd.write(chunk)
            fd.close()

            try:
                # 使用 xlrd 打开 excel 文件
                excelFiile = xlrd.open_workbook(os.path.join(FILE_ROOT, file.name))

                # 选择第一个 sheet
                table = excelFiile.sheets()[0]

                # 日期
                date = request.POST.get('date', None)
                if date == '':
                    date = datetime.datetime.now().strftime("%Y-%m")

                # 根据 table 的行数循环
                for i in range(table.nrows):

                    if self.isNum(table.cell_value(i, 0)):
                        medical = Medical()
                        medical.user = UserProfile.objects.get(name=table.cell_value(i, 1))
                        medical.date = datetime.datetime.strptime(date, "%Y-%m")
                        medical.salary = table.cell_value(i, 2)
                        medical.save()
            except Exception as e:
                print e

    # 未休年休假工资报酬发放
    def vacationFile(self, request):
        # 保存文件
        file = request.FILES.get('vacation', None)
        if file:
            fd = open(os.path.join(FILE_ROOT, file.name), 'wb+')
            for chunk in file.chunks():
                fd.write(chunk)
            fd.close()

            try:
                # 使用 xlrd 打开 excel 文件
                excelFiile = xlrd.open_workbook(os.path.join(FILE_ROOT, file.name))

                # 选择第一个 sheet
                table = excelFiile.sheets()[0]

                # 日期
                date = request.POST.get('date', None)
                if date == '':
                    date = datetime.datetime.now().strftime("%Y-%m")

                # 根据 table 的行数循环
                for i in range(table.nrows):

                    if self.isNum(table.cell_value(i, 0)):
                        tackholiday = TackHoliday()
                        # 姓名
                        tackholiday.user = UserProfile.objects.get(name=table.cell_value(i, 1))
                        tackholiday.date = datetime.datetime.strptime(date, "%Y-%m")
                        # 金额
                        tackholiday.salary = table.cell_value(i, 6)
                        tackholiday.save()

            except Exception as e:
                print e

    # 独生子女费
    def onlyFile(self, request):
        file = request.FILES.get('only', None)
        if file:
            fd = open(os.path.join(FILE_ROOT, file.name), 'wb+')
            for chunk in file.chunks():
                fd.write(chunk)
            fd.close()

            try:
                # 使用 xlrd 打开 excel 文件
                excelFiile = xlrd.open_workbook(os.path.join(FILE_ROOT, file.name))

                # 选择第一个 sheet
                table = excelFiile.sheets()[0]

                # 日期
                date = request.POST.get('date', None)
                if date == '':
                    date = datetime.datetime.now().strftime("%Y-%m")

                # 根据 table 的行数循环
                for i in range(table.nrows):

                    if self.isNum(table.cell_value(i, 0)):
                        singlechild = SingleChild()
                        # 姓名
                        singlechild.user = UserProfile.objects.get(name=table.cell_value(i, 1))
                        singlechild.date = datetime.datetime.strptime(date, "%Y-%m")
                        # 金额
                        singlechild.salary = table.cell_value(i, 7)
                        singlechild.save()

            except Exception as e:
                print e

    # 绩效考核奖发放
    def performanceAppraisaFile(self, request):
        # 保存文件
        file = request.FILES.get('performanceAppraisa', None)
        if file:
            fd = open(os.path.join(FILE_ROOT, file.name), 'wb+')
            for chunk in file.chunks():
                fd.write(chunk)
            fd.close()

            try:
                # 使用 xlrd 打开 excel 文件
                excelFiile = xlrd.open_workbook(os.path.join(FILE_ROOT, file.name))

                # 选择第一个 sheet
                table = excelFiile.sheets()[0]

                # 日期
                date = request.POST.get('date', None)
                if date == '':
                    date = datetime.datetime.now().strftime("%Y-%m")

                # 根据 table 的行数循环
                for i in range(table.nrows):

                    if self.isNum(table.cell_value(i, 0)):
                        performanceAppraisa = PerformanceAppraisa()
                        # 姓名
                        performanceAppraisa.user = UserProfile.objects.get(name=table.cell_value(i, 1))
                        performanceAppraisa.date = datetime.datetime.strptime(date, "%Y-%m")
                        # 2.5倍考核奖
                        performanceAppraisa.award = table.cell_value(i, 6)
                        # 所得税
                        performanceAppraisa.tax = table.cell_value(i, 9)
                        # 实发合计
                        performanceAppraisa.salary = table.cell_value(i, 10)
                        performanceAppraisa.save()
            except Exception as e:
                print e

    # 非统发人员工资及统发人员津贴发放
    def nonStaffFile(self, request):
        # 保存文件
        file = request.FILES.get('nonStaff', None)
        if file:
            fd = open(os.path.join(FILE_ROOT, file.name), 'wb+')
            for chunk in file.chunks():
                fd.write(chunk)
            fd.close()

            try:
                # 使用 xlrd 打开 excel 文件
                excelFiile = xlrd.open_workbook(os.path.join(FILE_ROOT, file.name))

                # 选择第一个 sheet
                table = excelFiile.sheets()[0]

                # 日期
                date = request.POST.get('date', None)
                if date == '':
                    date = datetime.datetime.now().strftime("%Y-%m")

                isName = False

                # 根据 table 的行数循环
                for i in range(table.nrows):

                    if isName:
                        nonstaff = NonStaff()
                        # 姓名
                        nonstaff.user = UserProfile.objects.get(name=table.cell_value(i, 0))
                        nonstaff.date = datetime.datetime.strptime(date, "%Y-%m")
                        # 年金
                        nonstaff.salary = table.cell_value(i, 38)
                        # 个人统筹医疗
                        nonstaff.medical = table.cell_value(i, 39)
                        # 养老补差
                        nonstaff.old = table.cell_value(i, 40)
                        # 住房公积金（个人）
                        nonstaff.house_p = table.cell_value(i, 41)
                        # 住房公积金（单位）
                        nonstaff.house_o = table.cell_value(i, 42)
                        # 房改住房补贴
                        nonstaff.house_fix = table.cell_value(i, 43)
                        nonstaff.save()

                    if table.cell_value(i, 0) == "姓名":
                        isName = True

            except Exception as e:
                print e

    # 过节费
    def holidayFile(self, request):
        file = request.FILES.get('holiday', None)
        if file:
            fd = open(os.path.join(FILE_ROOT, file.name), 'wb+')
            for chunk in file.chunks():
                fd.write(chunk)
            fd.close()

            try:
                # 使用 xlrd 打开 excel 文件
                excelFiile = xlrd.open_workbook(os.path.join(FILE_ROOT, file.name))

                # 选择第一个 sheet
                table = excelFiile.sheets()[0]

                # 日期
                date = request.POST.get('date', None)
                if date == '':
                    date = datetime.datetime.now().strftime("%Y-%m")

                isName = False

                # 根据 table 的行数循环
                for i in range(table.nrows):

                    if isName:
                        holiday = Holiday()
                        # 具体节日
                        holiday.holiday = table.cell_value(0, 0)[13:-1]
                        # 姓名
                        holiday.user = UserProfile.objects.get(name=table.cell_value(i, 0))
                        holiday.date = datetime.datetime.strptime(date, "%Y-%m")
                        # 金额
                        holiday.salary = table.cell_value(i, 18)
                        holiday.save()

                    if table.cell_value(i, 0) == "姓名":
                        isName = True

            except Exception as e:
                print e

    # 基层补贴
    def basicFile(self, request):
        file = request.FILES.get('basic', None)
        if file:
            fd = open(os.path.join(FILE_ROOT, file.name), 'wb+')
            for chunk in file.chunks():
                fd.write(chunk)
            fd.close()

            try:
                # 使用 xlrd 打开 excel 文件
                excelFiile = xlrd.open_workbook(os.path.join(FILE_ROOT, file.name))

                # 选择第一个 sheet
                table = excelFiile.sheets()[0]

                # 日期
                date = request.POST.get('date', None)
                if date == '':
                    date = datetime.datetime.now().strftime("%Y-%m")

                isName = False

                # 根据 table 的行数循环
                for i in range(table.nrows):

                    if isName:
                        basic = Basic()
                        # 姓名
                        basic.user = UserProfile.objects.get(name=table.cell_value(i, 0))
                        basic.date = datetime.datetime.strptime(date, "%Y-%m")
                        # 金额
                        basic.salary = table.cell_value(i, 18)
                        basic.save()

                    if table.cell_value(i, 0) == "姓名":
                        isName = True

            except Exception as e:
                print e

    # 养老保险临时补贴
    def oldFile(self, request):
        file = request.FILES.get('old', None)
        if file:
            fd = open(os.path.join(FILE_ROOT, file.name), 'wb+')
            for chunk in file.chunks():
                fd.write(chunk)
            fd.close()

            try:
                # 使用 xlrd 打开 excel 文件
                excelFiile = xlrd.open_workbook(os.path.join(FILE_ROOT, file.name))

                # 选择第一个 sheet
                table = excelFiile.sheets()[0]

                # 日期
                date = request.POST.get('date', None)
                if date == '':
                    date = datetime.datetime.now().strftime("%Y-%m")

                isName = False

                # 根据 table 的行数循环
                for i in range(table.nrows):

                    if isName:
                        provide = Provide()
                        # 补贴名称
                        #print table.cell_value(0, 0)[13:-1]
                        # 姓名
                        provide.user = UserProfile.objects.get(name=table.cell_value(i, 0))
                        provide.date = datetime.datetime.strptime(date, "%Y-%m")
                        # 金额
                        provide.salary = table.cell_value(i, 18)
                        provide.save()

                    if table.cell_value(i, 0) == "姓名":
                        isName = True

            except Exception as e:
                print e

    # 补发考核奖
    def performanceAppraisaFixFile(self, request):
        file = request.FILES.get('performanceAppraisaFix', None)
        if file:
            fd = open(os.path.join(FILE_ROOT, file.name), 'wb+')
            for chunk in file.chunks():
                fd.write(chunk)
            fd.close()

            try:
                # 使用 xlrd 打开 excel 文件
                excelFiile = xlrd.open_workbook(os.path.join(FILE_ROOT, file.name))

                # 选择第一个 sheet
                table = excelFiile.sheets()[0]

                # 日期
                date = request.POST.get('date', None)
                if date == '':
                    date = datetime.datetime.now().strftime("%Y-%m")

                isName = False

                # 根据 table 的行数循环
                for i in range(table.nrows):

                    if isName:
                        assess = Assess()
                        # 姓名
                        assess.user = UserProfile.objects.get(name=table.cell_value(i, 0))
                        assess.date = datetime.datetime.strptime(date, "%Y-%m")
                        # 金额
                        assess.salary = table.cell_value(i, 18)
                        assess.save()

                    if table.cell_value(i, 0) == "姓名":
                        isName = True

            except Exception as e:
                print e