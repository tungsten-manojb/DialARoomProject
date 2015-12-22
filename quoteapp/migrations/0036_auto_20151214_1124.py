# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0035_auto_20151214_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationresponse',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 24, 34, 243828), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_request_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 24, 34, 242669), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='requestedproperty',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 24, 34, 244683), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='userrequeststatistictrack',
            name='current_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 24, 34, 245298), verbose_name=b'Current Time Stamp'),
        ),
    ]
