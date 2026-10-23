from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='ti ti-category')
    color = models.CharField(max_length=30, default='blue')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Subscription(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    description = models.TextField(blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Каталог подписок'

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активна'),
        ('frozen', 'Заморожена'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_subscriptions'
    )

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='users'
    )

    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='active'
    )

    connected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'подписка пользователя'
        verbose_name_plural = 'Мои подписки'

    def __str__(self):
        return f'{self.user} — {self.subscription}'

    def get_status_display(self):
        pass
