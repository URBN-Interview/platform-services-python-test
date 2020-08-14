from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.RewardsView.as_view(), name='rewards'),
    url(r'info', views.AddInfo.as_view(), name='info'),
    # url(r'/getone', views.CustomerSummary.as_view(), name='rewards'),
    url(r'getall', views.UserRewards.as_view(), name='get_all')
]
