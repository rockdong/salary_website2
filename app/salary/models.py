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
    title = models.CharField(default='预发年终绩效工资', max_length=100)
    standard = models.FloatField(default=0.0, verbose_name='标准')
    amount = models.FloatField(default=0.0, verbose_name='金额')
    index = models.FloatField(default=0.0, verbose_name='数量')
    tax = models.FloatField(default=0.0, verbose_name='所得税')
    other = models.FloatField(default=0.0, verbose_name='其它补贴')


'''
政府绩效考核奖
'''
class GovPerformanceAppraisa(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    title = models.CharField(default='政府绩效考核奖', max_length=100)
    standard = models.FloatField(default=0.0, verbose_name='标准')
    amount = models.FloatField(default=0.0, verbose_name='金额')
    ratio = models.FloatField(default=0.0, verbose_name='系数')
    tax = models.FloatField(default=0.0, verbose_name='所得税')
    other = models.FloatField(default=0.0, verbose_name='扣除其它')


'''
特别效益奖励
'''
class SpecialBenefitAward(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    title = models.CharField(default='特别效益奖励性绩效', max_length=100)
    standard = models.FloatField(default=0.0, verbose_name='标准')
    index = models.FloatField(default=0.0, verbose_name='数量')
    amount = models.FloatField(default=0.0, verbose_name='金额')
    tax = models.FloatField(default=0.0, verbose_name='所得税')
    other = models.FloatField(default=0.0, verbose_name='其它补贴')


'''
干部职务奖励性绩效
'''
class CadreDutyAward(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    title = models.CharField(default='干部职务奖励性绩效', max_length=100)
    standard = models.FloatField(default=0.0, verbose_name='标准')
    subsidy = models.FloatField(default=0.0, verbose_name='补贴')
    index = models.FloatField(default=0.0, verbose_name='数量')
    tax = models.FloatField(default=0.0, verbose_name='所得税')
    other = models.FloatField(default=0.0, verbose_name='其它补贴')


'''
正式工资
'''
class ReallySalary(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    title = models.CharField(default='编内正式工工资', max_length=100)
    post_wage = models.FloatField(default=0.0, verbose_name='岗位工资')
    level_wage = models.FloatField(default=0.0, verbose_name='薪级工资')
    area_allowance = models.FloatField(default=0.0, verbose_name='特区津贴')
    base_allowance = models.FloatField(default=0.0, verbose_name='基础津贴')
    special_post_allowance = models.FloatField(default=0.0, verbose_name='特殊岗位津贴')
    shortage_post = models.FloatField(default=0.0, verbose_name='紧缺岗位')
    nursing_age = models.IntegerField(default=0, verbose_name='护龄')
    urance_benefit = models.FloatField(default=0.0, verbose_name='保险金')
    housing_fund = models.FloatField(default=0.0, verbose_name='住房公积金')
    housing_fund2 = models.FloatField(default=0.0, verbose_name='住房公积金2')
    tax = models.FloatField(default=0.0, verbose_name='所得税')
    rent = models.FloatField(default=0.0, verbose_name='房租')
    utilities = models.FloatField(default=0.0, verbose_name='水电')
    other = models.FloatField(default=0.0, verbose_name='其它')

'''
伙食
'''
class Food(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    title = models.CharField(default='院陪伙食补', max_length=100)
    date = models.DateField(verbose_name='日期')
    standard = models.FloatField(default=0.0, verbose_name='标准')
    amount = models.FloatField(default=0.0, verbose_name='金额')
    index = models.IntegerField(default=1, verbose_name='数量')
    tax = models.FloatField(default=0.0, verbose_name='所得税')

#----------------------------------------

'''
统筹医疗发放
'''
class Medical(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary = models.FloatField(default=0.0, verbose_name='应发金额')

'''
未休年休假工资报酬发放
'''
class TackHoliday(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary = models.FloatField(default=0.0, verbose_name='应支付未休年休假工资报酬')

'''
节日补贴
'''
class Holiday(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    holiday = models.CharField(max_length=20, verbose_name='节日')
    salary = models.FloatField(default=0.0, verbose_name='节日补贴')

'''
独生子女优待费发放
'''
class SingleChild(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary = models.FloatField(default=0.0, verbose_name='应发金额')

'''
绩效考核奖发放
'''
class PerformanceAppraisa(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    tax = models.FloatField(default=0.0, verbose_name='所得税')
    award = models.FloatField(default=0.0, verbose_name='2.5倍考核奖')
    salary = models.FloatField(default=0.0, verbose_name='实发合计')

'''
非统发人员工资及统发人员津贴发放
'''
class NonStaff(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary = models.FloatField(default=0.0, verbose_name='年金')
    medical = models.FloatField(default=0.0, verbose_name='个人统筹医疗')
    old = models.FloatField(default=0.0, verbose_name='养老补差')
    house_p = models.FloatField(default=0.0, verbose_name='住房公积金（个人）')
    house_o = models.FloatField(default=0.0, verbose_name='住房公积金（单位）')
    house_fix = models.FloatField(default=0.0, verbose_name='房改住房补贴')

'''
补发考核奖发放
'''
class Assess(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary = models.FloatField(default=0.0, verbose_name='年度考核奖')

'''
养老保险临时补贴
'''
class Provide(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary = models.FloatField(default=0.0, verbose_name='养老保险临时补贴')

'''
基层补贴
'''
class Basic(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    date = models.DateField(verbose_name='日期')
    salary = models.FloatField(default=0.0, verbose_name='基层补贴')