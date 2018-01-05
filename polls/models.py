from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from .managers import DiscountCodeManager, ClientManager


class DiscountCode(models.Model):
    code = models.CharField('Kod rabatowy', max_length=1000)
    is_active = models.BooleanField('Aktywny', default=True)

    objects = DiscountCodeManager()


class Client(models.Model):
    email = models.EmailField('E-mail', max_length=100)
    fb_id = models.CharField('Facebook ID', unique=True, max_length=100)
    added_time = models.DateTimeField('Data dodania', default=timezone.now)
    discount_code = models.ForeignKey(
        DiscountCode, on_delete=models.CASCADE, verbose_name='Kod rabatowy', blank=True, null=True
    )

    objects = ClientManager()
