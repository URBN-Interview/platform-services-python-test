from django.urls import include, re_path
from rewards import views

urlpatterns = [
    re_path(r'^$', views.RewardsView.as_view(), name='rewards'),
]
