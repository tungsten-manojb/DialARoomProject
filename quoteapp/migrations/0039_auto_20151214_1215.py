# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0038_auto_20151214_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationresponse',
            name='property_rack_rate',
            field=models.FloatField(default=0.0, null=True, verbose_name=b'Rack Rate Per Night', blank=True),
        ),
        migrations.AlterField(
            model_name='quotationresponse',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 12, 15, 11, 949548), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_request_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 12, 15, 11, 948217), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='requestedproperty',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 12, 15, 11, 950484), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='userrequeststatistictrack',
            name='current_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 12, 15, 11, 951081), verbose_name=b'Current Time Stamp'),
        ),
    ]
