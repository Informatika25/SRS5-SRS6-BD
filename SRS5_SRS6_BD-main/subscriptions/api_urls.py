from rest_framework.routers import DefaultRouter
from .api_views import CategoryViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = router.urls