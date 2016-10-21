from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.loadData, name='index'),
    url(r'sendMail', views.sendMail, name='sendMail'),
]