from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.RewardsView.as_view(), name='rewards'),
    url(r'^add_order/$', views.AddOrderView.as_view(), name='add_order')
    # url(r'^add_order/<str:email>/<int:order_total>$', views.AddOrderView.as_view(), name='add_order')
]
