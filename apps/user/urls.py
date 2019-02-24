from django.conf.urls import url
from user.views import RegisterView, LoginView, ActiveView, UserInfoView, UserOrderView, UserAddressView
from user import views

urlpatterns = [
    # url(r'^register$', views.register, name='register'),
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),
    url(r'^login$', LoginView.as_view(), name='login'),

    url(r'^$', UserInfoView.as_view(), name='user'),
    url(r'^order$', UserOrderView.as_view(), name='order'),
    url(r'^address$', UserAddressView.as_view(), name='address'),
]
