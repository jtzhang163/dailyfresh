from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse # 反向解析生成首页对应的地址
# from django.core.mail import send_mail
from django.views.generic import View # 使用类视图
from django.http import HttpResponse
from user.models import User
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth import authenticate, login
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
import re

# Create your views here.


# /user/register
# def register(request):
#
#     if request.method == 'GET':
#         # 显示注册页面
#         return render(request, "register.html")
#     else:
#         # 注册逻辑处理
#         username = request.POST.get('user_name')
#         password = request.POST.get('pwd')
#         email = request.POST.get('email')
#         allow = request.POST.get('allow')
#
#         if not all([username, password, email]):
#             return render(request, 'register.html', {'errmsg': '数据不完整'})
#
#         if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#             return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
#
#         if allow != 'on':
#             return render(request, 'register.html', {'errmsg': '请同意协议'})
#
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             user = None
#
#         if user:
#             return render(request, 'register.html', {'errmsg': '用户已存在'})
#
#         # user = User()
#         # user.username = username
#         # user.password = password
#         # user.email = email
#         #
#         # user.save()
#
#         user = User.objects.create_user(username, email, password)
#         user.is_active = 0
#         user.save()
#
#         return redirect(reverse('goods:index'))

# /user/register
class RegisterView(View):
    """注册"""
    def get(self, request):
        """显示注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """进行注册处理"""
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

        # 生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # bytes 字节流
        token = token.decode()  # 相当于decode('utf8')

        # 发送激活邮件

        send_register_active_email.delay(email, username, token)

        # subject = '天天生鲜激活链接'
        # message = ''
        # sender = settings.EMAIL_FROM
        # receiver = [email]
        # html_message = '<h1>%s, 欢迎你成为天天生鲜的注册会员</h1> 请点击下面的链接激活您的账户: <br /><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)
        # send_mail(subject, message, sender, receiver, html_message=html_message)

        return redirect(reverse('goods:index'))


class ActiveView(View):
    """用户激活"""
    def get(self, request, token):

        # 解密token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']

            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            return HttpResponse('激活链接已过期')


# /user/login
class LoginView(View):

    def get(self, request):
        '''显示登录页面'''
        return render(request, 'login.html')

    def post(self, request):
        '''进行登录处理'''
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整! '})

        # https://yiyibooks.cn/xx/Django_1.11.6/topics/auth/default.html
        # from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)  # 记录用户的登录状态
                return redirect(reverse('goods:index'))
            else:
                return render(request, 'login.html', {'errmsg': '账户未激活! '})
        else:
            return render(request, 'login.html', {'errmsg': '用户名或密码错误! '})







