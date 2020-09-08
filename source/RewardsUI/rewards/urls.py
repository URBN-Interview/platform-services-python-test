from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.RewardsView.as_view(), name='rewards'),
    #url(r'^$', views.RewardsView.as_view(), name='allCustomers'),
    #url(r'^$', views.RewardsView.as_view(), name='/order/(.*)'),
    #url(r'^$', views.RewardsView.as_view(), name='/customer/(.*)'),
]
