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
    category_color = serializers.CharField(
        source='category.color',
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
            'category_color',
        ]

    def validate_name(self, value):
        val = value.strip()
        if not val:
            raise serializers.ValidationError('Название подписки не может быть пустым.')
        if len(val) < 2:
            raise serializers.ValidationError('Название должно содержать не менее 2 символов.')
        return val

    def validate_price(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError('Цена подписки должна быть больше 0.')
        return value