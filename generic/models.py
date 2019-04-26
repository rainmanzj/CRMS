from django.db import models
from rbac.models import User as RbacUser


# Create your models here.

class School(models.Model):
    """
    校区表
    """
    title = models.CharField(verbose_name='校区名', max_length=32)

    def __str__(self):
        return self.title


class DepartMent(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='部门', max_length=32)

    def __str__(self):
        return self.title


class Staffinfo(RbacUser):
    """
    职工表
    """

    realname = models.CharField(verbose_name='真实姓名', max_length=32)
    phone = models.CharField(verbose_name='手机号', max_length=11)
    gender_choices = ((1, '男'), (2, '女'), (3, '其他'))
    gender = models.IntegerField(verbose_name='性别', choices=gender_choices)
    depart = models.ForeignKey(verbose_name='部门', to=DepartMent, on_delete='cascade')

    def __str__(self):
        return self.username
