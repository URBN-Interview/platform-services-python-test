from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.RewardsView.as_view(), name='rewards'),
    url(r'^add_order/$', views.AddOrderView.as_view(), name='add_order'),
    url(r'^search_user/$', views.SearchUserView.as_view(), name='search_user'),
] 

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
