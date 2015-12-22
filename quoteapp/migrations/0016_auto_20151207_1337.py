# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0015_auto_20151203_0535'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestedproperty',
            name='quoted_status',
            field=models.BooleanField(default=False, verbose_name=b'Quotation Status'),
        ),
        migrations.AlterField(
            model_name='quotationresponse',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 7, 13, 37, 15, 649120), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_request_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 7, 13, 37, 15, 647479), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='requestedproperty',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 7, 13, 37, 15, 650806), null=True, verbose_name=b'Update Date', blank=True),
        ),
    ]
