from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('my-subscriptions/',views.my_subscriptions,name='my_subscriptions'),
    path('my-subscriptions/<int:subscription_id>/change-status/',views.change_subscription_status,name='change_subscription_status'),
    path('catalog/<int:subscription_id>/subscribe/',views.subscribe,name='subscribe'),
    path('my-subscriptions/<int:subscription_id>/cancel/',views.cancel_subscription,name='cancel_subscription'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('management/', views.subscription_management, name='subscription_management'),
]