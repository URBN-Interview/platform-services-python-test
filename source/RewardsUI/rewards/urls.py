from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.RewardsView.as_view(), name='rewards'),
]
