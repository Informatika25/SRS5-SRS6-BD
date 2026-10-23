from rest_framework import serializers
from .models import Category, Subscription


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    class Meta:
        model = Subscription
        fields = [
            'id',
            'name',
            'price',
            'description',
            'category',
            'category_name',
        ]