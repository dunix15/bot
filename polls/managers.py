from django.db.models import Manager

from .queryset import DiscountCodeQuerySet, ClientQuerySet


class DiscountCodeBaseManager(Manager):
    pass


DiscountCodeManager = DiscountCodeBaseManager.from_queryset(DiscountCodeQuerySet)


class ClientBaseManager(Manager):
    pass


ClientManager = ClientBaseManager.from_queryset(ClientQuerySet)
