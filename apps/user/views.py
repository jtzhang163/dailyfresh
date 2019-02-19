from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse # 反向解析生成首页对应的地址
from user.models import User
import re

# Create your views here.
# /user/register


def register(request):

    if request.method == 'GET':
        # 显示注册页面
        return render(request, "register.html")
    else:
        # 注册逻辑处理
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', {'errmsg': '用户已存在'})

        # user = User()
        # user.username = username
        # user.password = password
        # user.email = email
        #
        # user.save()

        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        return redirect(reverse('goods:index'))


