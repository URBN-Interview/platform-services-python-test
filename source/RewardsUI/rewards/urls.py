from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    url(r'', views.RewardsView.as_view(), name='rewards'),
    #url(r'customer_rewards', views.customer_rewards, name='customer_rewards'),
]