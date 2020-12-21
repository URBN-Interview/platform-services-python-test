from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.RewardsView.as_view(), name='rewards'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)