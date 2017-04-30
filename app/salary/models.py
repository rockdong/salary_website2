# _*_ coding:utf-8 _*_

from __future__ import unicode_literals

from django.db import models

from user_profile.models import UserProfile

# Create your models here.


# class Salary(models.Model):
#     user = models.ForeignKey(UserProfile, verbose_name='用户')
#     date = models.DateField(verbose_name='时间')
#     realy_salary = models.FloatField(verbose_name='应发工资')
#     realy_discount = models.FloatField(verbose_name='应扣金额')
#     replacement_amount = models.FloatField(verbose_name='补发金额')
#
#     class Meta:
#         verbose_name = '工资'
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return self.user.name + "|" + self.date + "|" + self.realy_salary
#
#
# class DetailSalary(models.Model):
#     user = models.ForeignKey(UserProfile, verbose_name='用户')
#     content = models.CharField(max_length=100, verbose_name='内容')
#     realy_salary = models.FloatField(verbose_name='应发工资')
#     realy_discount = models.FloatField(verbose_name='应扣金额')
#     replacement_amount = models.FloatField(verbose_name='补发金额')
#
#     class Meta:
#         verbose_name = '工资明细'
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return self.user.name + "|" + self.user.date + "|" + self.content
#
#
# class DetailPart(models.Model):
#     detail_salary = models.ForeignKey(DetailSalary, verbose_name='工资明细')
#     standard = models.FloatField(verbose_name='标准')
#     tax = models.FloatField(verbose_name='所得税')
#     really_salary = models.FloatField(verbose_name='实发合计')
#
#     class Meta:
#         verbose_name = '工资详情'
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return self.detail_salary.user.name + "|"


'''
预发年终绩效奖励
'''
class PreYearEndPerformanceAppraisa(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    standard = models.FloatField(verbose_name='标准')
    index = models.FloatField(verbose_name='数量')
    tax = models.FloatField(verbose_name='所得税')
    other = models.FloatField(verbose_name='其它补贴')


'''
政府绩效考核奖
'''
class GovPerformanceAppraisa(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    standard = models.FloatField(verbose_name='标准')
    amount = models.FloatField(verbose_name='金额')
    ratio = models.FloatField(verbose_name='系数')
    tax = models.FloatField(verbose_name='所得税')
    other = models.FloatField(verbose_name='扣除其它')


'''
特别效益奖励
'''
class SpecialBenefitAward(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    standard = models.FloatField(verbose_name='标准')
    index = models.FloatField(verbose_name='数量')
    tax = models.FloatField(verbose_name='所得税')
    other = models.FloatField(verbose_name='其它补贴')


'''
干部职务奖励性绩效
'''
class CadreDutyAward(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    standard = models.FloatField(verbose_name='标准')
    subsidy = models.FloatField(verbose_name='补贴')
    index = models.FloatField(verbose_name='数量')
    tax = models.FloatField(verbose_name='所得税')
    other = models.FloatField(verbose_name='其它补贴')


'''
正式工资
'''
class ReallySalary(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    post_wage = models.FloatField(verbose_name='岗位工资')
    level_wage = models.FloatField(verbose_name='薪级工资')
    area_allowance = models.FloatField(verbose_name='特区津贴')
    base_allowance = models.FloatField(verbose_name='基础津贴')
    special_post_allowance = models.FloatField(verbose_name='特殊岗位津贴')
    shortage_post = models.FloatField(verbose_name='紧缺岗位')
    nursing_age = models.IntegerField(verbose_name='护龄')
    urance_benefit = models.FloatField(verbose_name='保险金')
    housing_fund = models.FloatField(verbose_name='住房公积金')
    housing_fund2 = models.FloatField(verbose_name='住房公积金2')
    tax = models.FloatField(verbose_name='所得税')
    rent = models.FloatField(verbose_name='房租')
    utilities = models.FloatField(verbose_name='水电')
    other = models.FloatField(verbose_name='其它')

'''
伙食
'''
class Food(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    standard = models.FloatField(verbose_name='标准')
    amount = models.FloatField(verbose_name='金额')
    index = models.IntegerField(verbose_name='数量')
    tax = models.FloatField(verbose_name='所得税')