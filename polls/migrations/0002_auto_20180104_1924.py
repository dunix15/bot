# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-04 19:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='discount_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.DiscountCode', verbose_name='Kod rabatowy'),
        ),
    ]
