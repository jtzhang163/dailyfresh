from django.conf.urls import url
from user.views import RegisterView
from user import views

urlpatterns = [
    # url(r'^register$', views.register, name='register'),
    url(r'^register$', RegisterView.as_view(), name='register')
]
