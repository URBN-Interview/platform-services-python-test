from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.RewardsView.as_view(), name='rewards'),
    url(r'^delete_product', views.ClientRewardsView.get, name='delete_product')
]
