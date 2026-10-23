from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import Subscription, UserSubscription

def home(request):
    return render(request, 'home.html')


def catalog(request):
    subscriptions = Subscription.objects.select_related(
        'category'
    ).all()

    return render(
        request,
        'catalog.html',
        {'subscriptions': subscriptions}
    )



@login_required
def my_subscriptions(request):
    user_subscriptions = UserSubscription.objects.select_related(
        'subscription',
        'subscription__category',
    ).filter(user=request.user)

    return render(
        request,
        'my_subscriptions.html',
        {'user_subscriptions': user_subscriptions}
    )



@login_required
@require_POST
def change_subscription_status(request, subscription_id):
    user_subscription = get_object_or_404(
        UserSubscription,
        id=subscription_id,
        user=request.user
    )

    if user_subscription.status == 'active':
        user_subscription.status = 'frozen'
    else:
        user_subscription.status = 'active'

    user_subscription.save(update_fields=['status'])

    return JsonResponse({
        'status': user_subscription.status,
        'status_display': user_subscription.get_status_display(),
    })






@login_required
@require_POST
def subscribe(request, subscription_id):
    subscription = get_object_or_404(
        Subscription,
        id=subscription_id
    )

    user_subscription, created = UserSubscription.objects.get_or_create(
        user=request.user,
        subscription=subscription,
        defaults={'status': 'active'}
    )

    if not created:
        return JsonResponse({
            'success': False,
            'message': 'Эта подписка уже есть в твоём списке.'
        }, status=400)

    return JsonResponse({
        'success': True,
        'message': 'Подписка успешно подключена!'
    })

@login_required
@require_POST
def cancel_subscription(request, subscription_id):
    user_subscription = get_object_or_404(
        UserSubscription,
        id=subscription_id,
        user=request.user
    )

    subscription_name = user_subscription.subscription.name
    user_subscription.delete()

    return JsonResponse({
        'success': True,
        'message': f'Подписка «{subscription_name}» отменена.'
    })


@login_required
def dashboard(request):
    from django.db.models import Sum, Count

    active_subscriptions = UserSubscription.objects.filter(
        user=request.user,
        status='active'
    )

    total_expenses = active_subscriptions.aggregate(
        total=Sum('subscription__price')
    )['total'] or 0

    active_count = active_subscriptions.count()

    category_stats = (
        active_subscriptions
        .values('subscription__category__name')
        .annotate(
            total=Sum('subscription__price'),
            count=Count('id')
        )
        .order_by('-total')
    )

    return render(request, 'dashboard.html', {
        'total_expenses': total_expenses,
        'active_count': active_count,
        'category_stats': category_stats,
    })
