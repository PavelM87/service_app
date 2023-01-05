from django.db.models import Prefetch, F
from rest_framework.viewsets import ReadOnlyModelViewSet

from services.models import Subscription
from services.serializers import SubscriptionSerializer
from clients.models import Client


class SubscriptionView(ReadOnlyModelViewSet):
    # queryset = Subscription.objects.all().prefetch_related('client').prefetch_related('client__user')
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name','user__email'))
    ).annotate(
        price=F('service__full_price') - F('service__full_price') * F('plan__discount_percent') / 100.00
    )
    serializer_class = SubscriptionSerializer


