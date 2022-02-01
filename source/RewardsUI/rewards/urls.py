from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.RewardsView.as_view(), name='rewards'),
    url(r'^$', views.RewardsView.as_view(), name='insert'),
    url(r'^$', views.RewardsView.as_view(), name='find'),
    url(r'^$', views.RewardsView.as_view(), name='all'),
    url(r'^$', views.RewardsView.as_view(), name='clear'),
]
