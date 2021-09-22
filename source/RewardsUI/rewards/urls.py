from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.RewardsView.as_view(), name='rewards'),
    url(r'^order/$', views.CustomerRewardsView.as_view(), name='customer-rewards'),
    url(r'^customer/$', views.CustomerRewardsView.as_view(), name='customer-rewards'),
    url(r'^customer/search/$', views.CustomerSearchView.as_view(), name='customer-rewards'),
]
