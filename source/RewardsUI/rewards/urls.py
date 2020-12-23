from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.RewardsView.as_view(), name='rewards'),
    url(r'^$', views.CustomerRewardsView.as_view(), name='customers')
]
