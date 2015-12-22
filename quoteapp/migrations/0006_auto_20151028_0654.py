# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0005_auto_20151023_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoterequest',
            name='property_rating',
            field=models.IntegerField(default=1, null=True, verbose_name=b'Property Rating', blank=True),
        ),
        migrations.AddField(
            model_name='quoterequest',
            name='quote_property_type',
            field=models.CharField(max_length=30, null=True, verbose_name=b'Property Type', blank=True),
        ),
        migrations.AlterField(
            model_name='quotationresponse',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 6, 54, 32, 92946), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_request_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 6, 54, 32, 91922), null=True, verbose_name=b'Update Date', blank=True),
        ),
    ]
