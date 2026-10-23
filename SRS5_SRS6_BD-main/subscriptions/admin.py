
from django.contrib import admin

from .models import Category, Subscription, UserSubscription


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon', 'color')
    search_fields = ('name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'subscription',
        'status',
        'connected_at',
    )
    list_filter = ('status', 'subscription__category')
    search_fields = (
        'user__username',
        'subscription__name',
    )
