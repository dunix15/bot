from django.contrib import admin

from .models import DiscountCode, Client


admin.site.register(DiscountCode)
admin.site.register(Client)
