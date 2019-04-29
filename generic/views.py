#! /usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import redirect, render
from generic.models import Staffinfo
from utils.md5 import gen_md5
from rbac.service.init_permission import init_permission


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    username = request.POST.get('username')
    password = gen_md5(request.POST.get('password'))
    current_user = Staffinfo.objects.filter(username=username, password=password).first()

    if not current_user:
        return render(request, 'login.html', {'error': '用户名或密码错误'})

    request.session['staffinfo'] = {'staff_id': current_user.id, 'realname': current_user.realname}
    # 用户权限信息的初始化
    init_permission(current_user, request)

    return redirect('/index/')


def logout(request):
    request.session.delete()
    return redirect('/login/')


def index(request):
    return render(request, 'index.html')
