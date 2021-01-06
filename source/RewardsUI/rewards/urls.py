from django.conf.urls import url

from . import views, customer_views

urlpatterns = [
    url(r'^$', views.RewardsView.as_view(), name='rewards'),
    url(r'^$', customer_views.CustomerRewardsView.as_view(), name='customers')
]
