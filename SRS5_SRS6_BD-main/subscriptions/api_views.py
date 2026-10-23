from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import ValidationError

from .models import Category, Subscription
from .serializers import CategorySerializer, SubscriptionSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Subscription.objects.select_related('category').all()

        # Фильтр по названию подписки
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        # Фильтр по категории
        category = self.request.query_params.get('category')
        if category:
            if not category.isdigit():
                raise ValidationError({
                    'category': 'Укажите корректный ID категории.'
                })
            queryset = queryset.filter(category_id=category)

        # Фильтр по максимальной цене
        max_price = self.request.query_params.get('max_price')
        if max_price:
            try:
                max_price = float(max_price)
                if max_price < 0:
                    raise ValueError
            except ValueError:
                raise ValidationError({
                    'max_price': 'Укажите неотрицательное число.'
                })
            queryset = queryset.filter(price__lte=max_price)

        # Сортировка (ordering)
        ordering = self.request.query_params.get('ordering', 'name')
        allowed_orderings = {
            'name': 'name',
            '-name': '-name',
            'price': 'price',
            '-price': '-price',
            'id': 'id',
            '-id': '-id',
        }
        order_by_field = allowed_orderings.get(ordering, 'name')

        return queryset.order_by(order_by_field)