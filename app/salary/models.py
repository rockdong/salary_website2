# _*_ coding:utf-8 _*_

from __future__ import unicode_literals

from django.db import models

from user_profile.models import UserProfile

# Create your models here.

'''
统筹医疗发放
'''
class Medical(models.Model):
    user = models.CharField(max_length=20, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary = models.FloatField(default=0.0, verbose_name='应发金额')

    def toString(self):
        return "<div class=\"form-group\"><span>应发金额 : </span><span>" + str(self.salary) + "</span></div>"

'''
未休年休假工资报酬发放
'''
class TackHoliday(models.Model):
    user = models.CharField(max_length=20, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary = models.FloatField(default=0.0, verbose_name='应支付未休年休假工资报酬')

    def toString(self):
        return "<div class=\"form-group\"><span>应支付未休年休假工资报酬 : </span><span>" + str(self.salary) + "</span></div>"

'''
节日补贴
'''
class Holiday(models.Model):
    user = models.CharField(max_length=20, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    holiday = models.CharField(max_length=20, verbose_name='节日')
    salary = models.FloatField(default=0.0, verbose_name='节日补贴')

    def toString(self):
        return "<div class=\"form-group\"><span>" + self.holiday + " : </span><span>" + str(self.salary) + "</span></div>"

'''
独生子女优待费发放
'''
class SingleChild(models.Model):
    user = models.CharField(max_length=20, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary = models.FloatField(default=0.0, verbose_name='应发金额')

    def toString(self):
        return "<div class=\"form-group\"><span>应发金额 : </span><span>" + str(self.salary) + "</span></div>"

'''
绩效考核奖发放
'''
class PerformanceAppraisa(models.Model):
    user = models.CharField(max_length=20, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    tax = models.FloatField(default=0.0, verbose_name='所得税')
    award = models.FloatField(default=0.0, verbose_name='2.5倍考核奖')
    salary = models.FloatField(default=0.0, verbose_name='实发合计')

    def toString(self):
        return "<div class=\"form-group\"><span>2.5倍考核奖 : </span><span>" + str(self.award) + "</span></div>" + \
               "<div class=\"form-group\"><span>所得税 : </span><span>" + str(self.tax) + "</span></div>" + \
               "<div class=\"form-group\"><span>实发合计 : </span><span>" + str(self.salary) + "</span></div>"

'''
非统发人员工资及统发人员津贴发放
'''
class NonStaff(models.Model):
    user = models.CharField(max_length=20, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary = models.FloatField(default=0.0, verbose_name='年金')
    medical = models.FloatField(default=0.0, verbose_name='个人统筹医疗')
    old = models.FloatField(default=0.0, verbose_name='养老补差')
    house_p = models.FloatField(default=0.0, verbose_name='住房公积金（个人）')
    house_o = models.FloatField(default=0.0, verbose_name='住房公积金（单位）')
    house_fix = models.FloatField(default=0.0, verbose_name='房改住房补贴')

    def toString(self):
        return "<div class=\"form-group\"><span>年金 : </span><span>" + str(self.salary) + "</span></div>" + \
               "<div class=\"form-group\"><span>个人统筹医疗 : </span><span>" + str(self.medical) + "</span></div>" + \
               "<div class=\"form-group\"><span>养老补差 : </span><span>" + str(self.old) + "</span></div>" + \
               "<div class=\"form-group\"><span>住房公积金（个人） : </span><span>" + str(self.house_p) + "</span></div>" + \
               "<div class=\"form-group\"><span>住房公积金（单位） : </span><span>" + str(self.house_o) + "</span></div>" + \
               "<div class=\"form-group\"><span>房改住房补贴 : </span><span>" + str(self.house_fix) + "</span></div>"

'''
补发考核奖发放
'''
class Assess(models.Model):
    user = models.CharField(max_length=20, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary = models.FloatField(default=0.0, verbose_name='年度考核奖')

    def toString(self):
        return "<div class=\"form-group\"><span>年度考核奖 : </span><span>" + str(self.salary) + "</span></div>"

'''
养老保险临时补贴
'''
class Provide(models.Model):
    user = models.CharField(max_length=20, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary = models.FloatField(default=0.0, verbose_name='养老保险临时补贴')

    def toString(self):
        return "<div class=\"form-group\"><span>养老保险临时补贴 : </span><span>" + str(self.salary) + "</span></div>"

'''
基层补贴
'''
class Basic(models.Model):
    user = models.CharField(max_length=20, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary = models.FloatField(default=0.0, verbose_name='基层补贴')

    def toString(self):
        return "<div class=\"form-group\"><span>基层补贴 : </span><span>" + str(self.salary) + "</span></div>"

'''
财政统发工资系统总表
'''
class Total(models.Model):
    user = models.CharField(max_length=20, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary_card = models.IntegerField(verbose_name='工资卡号')
    salary_job = models.FloatField(default=0.0, verbose_name='职务工资')
    salary_lv = models.FloatField(default=0.0, verbose_name='级别工资')
    salary_sp = models.FloatField(default=0.0, verbose_name='特区津贴')
    salary_bc = models.FloatField(default=0.0, verbose_name='基础津贴')
    salary_year_p = models.FloatField(default=0.0, verbose_name='职业年金个人')
    salary_year_o = models.FloatField(default=0.0, verbose_name='职业年金单位')
    salary_year = models.FloatField(default=0.0, verbose_name='年金')
    salary_assess = models.FloatField(default=0.0, verbose_name='奖励性绩效工资')
    salary_t = models.FloatField(default=0.0, verbose_name='应发工资')
    sp_salary = models.FloatField(default=0.0, verbose_name='个人缴纳社保费-个人合计')
    sp_medical = models.FloatField(default=0.0, verbose_name='个人缴纳社保费-个人医疗')
    sp_old = models.FloatField(default=0.0, verbose_name='个人缴纳社保费-个人养老')
    sp_medical_count = models.FloatField(default=0.0, verbose_name='个人缴纳社保费-个人统筹医疗')
    tax = models.FloatField(default=0.0, verbose_name='所得税')
    accumulation_p = models.FloatField(default=0.0, verbose_name='个人公积金')
    accumulation_o = models.FloatField(default=0.0, verbose_name='单位公积金')
    salary_r = models.FloatField(default=0.0, verbose_name='实发工资')
    house_fix = models.FloatField(default=0.0, verbose_name='房改补贴')
    so_salary = models.FloatField(default=0.0, verbose_name='单位缴纳社保费-单位社保合计')
    so_medical = models.FloatField(default=0.0, verbose_name='单位缴纳社保费-单位医疗')
    so_old = models.FloatField(default=0.0, verbose_name='单位缴纳社保费-单位养老')

    def toString(self):
        return "<div><span>职务工资 : </span><span>" + str(self.salary_job) + "</span></div>" + \
               "<div><span>级别工资 : </span><span>" + str(self.salary_lv) + "</span></div>" + \
               "<div><span>特区津贴 : </span><span>" + str(self.salary_sp) + "</span></div>" + \
               "<div><span>基础津贴 : </span><span>" + str(self.salary_bc) + "</span></div>" + \
               "<div><span>职业年金个人 : </span><span>" + str(self.salary_year_p) + "</span></div>" + \
               "<div><span>职业年金单位 : </span><span>" + str(self.salary_year_o) + "</span></div>" + \
               "<div><span>年金 : </span><span>" + str(self.salary_year) + "</span></div>" + \
               "<div><span>奖励性绩效工资 : </span><span>" + str(self.salary_assess) + "</span></div>" + \
               "<div><span>个人缴纳社保费-个人合计 : </span><span>" + str(self.sp_salary) + "</span></div>" + \
               "<div><span>个人缴纳社保费-个人医疗 : </span><span>" + str(self.sp_medical) + "</span></div>" + \
               "<div><span>个人缴纳社保费-个人养老 : </span><span>" + str(self.sp_old) + "</span></div>" + \
               "<div><span>个人缴纳社保费-个人统筹医疗 : </span><span>" + str(self.sp_medical_count) + "</span></div>" + \
               "<div><span>所得税 : </span><span>" + str(self.tax) + "</span></div>" + \
               "<div><span>个人公积金 : </span><span>" + str(self.accumulation_p) + "</span></div>" + \
               "<div><span>单位公积金 : </span><span>" + str(self.accumulation_o) + "</span></div>" + \
               "<div><span>房改补贴 : </span><span>" + str(self.house_fix) + "</span></div>" + \
               "<div><span>单位缴纳社保费-单位社保合计 : </span><span>" + str(self.so_salary) + "</span></div>" + \
               "<div><span>单位缴纳社保费-单位医疗 : </span><span>" + str(self.so_medical) + "</span></div>" + \
               "<div><span>单位缴纳社保费-单位养老 : </span><span>" + str(self.so_old) + "</span></div>" + \
               "<div><span>应发工资 : </span><span>" + str(self.salary_t) + "</span></div>" + \
               "<div><span>实发工资 : </span><span>" + str(self.salary_r) + "</span></div>"