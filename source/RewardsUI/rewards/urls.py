from django.conf.urls import url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
#from .views import get_customer_rewards

urlpatterns = [
    url(r'^$', csrf_exempt(views.RewardsView.as_view()), name='rewards'),
]

urlpatterns += staticfiles_urlpatterns()
