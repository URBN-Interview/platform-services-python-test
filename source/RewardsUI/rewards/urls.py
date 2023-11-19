from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.RewardsView.as_view(), name='rewards'),
    url(r'^order/$', views.CustomerOrderView.as_view(), name='submit_order'),
    url(r'^user/$', views.CustomerRewardsView.as_view(), name='user_rewards'),
]
