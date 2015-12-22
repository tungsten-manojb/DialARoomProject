# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0002_auto_20151019_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationresponse',
            name='quotation_uid',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Quote Remark', blank=True),
        ),
        migrations.AddField(
            model_name='quoterequest',
            name='quote_request_status',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'Quote Remark', choices=[(b'OPEN', b'OPEN'), (b'CLOSE', b'CLOSE')]),
        ),
        migrations.AlterField(
            model_name='quotationresponse',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 111520), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='customer_id',
            field=models.ForeignKey(related_name='customer_request', to='CorpRoomApp.Customer'),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_request_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 110499), null=True, verbose_name=b'Update Date', blank=True),
        ),
    ]
