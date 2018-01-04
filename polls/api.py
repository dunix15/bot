from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.routers import DefaultRouter
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from .models import DiscountCode, Client


class DiscountCodeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ('code', 'is_active')


class DiscountCodeViewSet(ModelViewSet):
    queryset = DiscountCode.objects.all()

    serializer_class = DiscountCodeSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    filter_fields = ('code', 'is_active')

    search_fields = ('code', 'is_active')

    ordering_fields = ('code', 'is_active')


class ClientSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ('email', 'added_time', 'discount_code')


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()

    serializer_class = ClientSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    filter_fields = ('email', 'added_time', 'discount_code')

    search_fields = ('email', 'added_time', 'discount_code')

    ordering_fields = ('added_time', 'discount_code')


router = DefaultRouter()
router.register(r'codes', DiscountCodeViewSet)
router.register(r'clients', ClientViewSet)
