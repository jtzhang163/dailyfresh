from django.conf import settings
from django.core.mail import send_mail
from celery import Celery
import time

# django环境的初始化,
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()


app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/8')

@app.task
def send_register_active_email(to_mail, username, token):
    '''发送激活邮件'''

    subject = '天天生鲜激活链接'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_mail]
    html_message = '<h1>%s, 欢迎你成为天天生鲜的注册会员</h1> 请点击下面的链接激活您的账户: <br /><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)