from startX.serivce.v1 import site, StartXHandler, StartXModelForm, get_field_display, Option, StarkForm
from generic import models
from django import forms
from django.forms import ValidationError
from utils.md5 import gen_md5
from django.shortcuts import HttpResponse, render, redirect
from django.urls import path, re_path
from django.utils.safestring import mark_safe


class SchoolHandler(StartXHandler):
    list_display = ['title']


class DepartMentHandler(StartXHandler):
    list_display = ['title']


site.register(models.School, SchoolHandler)
site.register(models.DepartMent, DepartMentHandler)


class StaffAddForm(StartXModelForm):
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.Staffinfo
        fields = ['username', 'realname', 'password', 'confirm_password', 'gender', 'email', 'phone', 'depart', 'roles']

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data


class ResetPasswordForm(StarkForm):
    """重置密码的form"""
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data


class StaffChangeModelForm(StartXModelForm):
    class Meta:
        model = models.Staffinfo
        fields = ['username', 'realname', 'gender', 'email', 'phone', 'depart', 'roles']


class StaffHandler(StartXHandler):
    search_list = ['username__contains', 'realname__contains']
    search_group = [
        Option('gender', is_multi=True),
        Option('depart'),
    ]

    def display_reset_pwd(self, model=None, is_header=None):
        """
        重置密码组件
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return '重置密码'
        # reset_url = self.reverse_commons_url(self.get_url_name('reset_pwd'), pk=model.pk)
        # return mark_safe("<a href='%s'>重置密码</a>" % reset_url)
        return mark_safe("<a href='#'>重置密码</a>")

    list_display = ['username', 'realname', get_field_display('性别', 'gender'), 'email', 'phone', 'depart', 'roles',
                    display_reset_pwd]

    def get_model_form(self, is_add=False):
        if is_add:
            return StaffAddForm
        return StaffChangeModelForm

    def reset_password(self, request, pk):
        """
        重置密码的视图函数
        :param request:
        :param pk:
        :return:
        """
        staffinfo_object = models.Staffinfo.objects.filter(id=pk).first()
        if not staffinfo_object:
            return HttpResponse('用户不存在，无法进行密码重置！')
        if request.method == 'GET':
            form = ResetPasswordForm()
            return render(request, 'startX/change.html', {'form': form})
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            staffinfo_object.password = form.cleaned_data['password']
            staffinfo_object.save()
            return redirect(self.reverse_list_url())
        return render(request, 'startX/change.html', {'form': form})

    def extra_urls(self):
        patterns = [
            re_path(r'^reset/password/(?P<pk>\d+)/$', self.wrapper(self.reset_password),
                    name=self.get_url_name('reset_pwd'))
        ]
        return patterns


site.register(models.Staffinfo, StaffHandler)
