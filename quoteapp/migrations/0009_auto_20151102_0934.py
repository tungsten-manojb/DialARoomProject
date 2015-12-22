# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0008_auto_20151102_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestedproperty',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='quotationresponse',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 2, 9, 34, 5, 323993), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_request_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 2, 9, 34, 5, 322986), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='requestedproperty',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 2, 9, 34, 5, 324861), null=True, verbose_name=b'Update Date', blank=True),
        ),
    ]
