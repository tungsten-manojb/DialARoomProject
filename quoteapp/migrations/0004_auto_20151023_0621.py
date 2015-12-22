# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0003_auto_20151020_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationresponse',
            name='is_new',
            field=models.BooleanField(default=True, verbose_name=b'Is New Quotation'),
        ),
        migrations.AlterField(
            model_name='quotationresponse',
            name='quotation_status',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Quatation Status', choices=[(b'VIEWED', b'VIEWED'), (b'QUOTED', b'QUOTED'), (b'EXPIRED', b'EXPIRED'), (b'INPROGRESS', b'INPROGRESS'), (b'SUBMITTED', b'SUBMITTED'), (b'REJECTED', b'REJECTED'), (b'ACCEPTED', b'ACCEPTED'), (b'CANCELLED', b'CANCELLED'), (b'BOOKED', b'BOOKED')]),
        ),
        migrations.AlterField(
            model_name='quotationresponse',
            name='quotation_uid',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Quotation UID', blank=True),
        ),
        migrations.AlterField(
            model_name='quotationresponse',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 23, 6, 21, 12, 619129), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_admin_status',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Quote ADMIN Status', choices=[(b'VIEWED', b'VIEWED'), (b'QUOTED', b'QUOTED'), (b'EXPIRED', b'EXPIRED'), (b'INPROGRESS', b'INPROGRESS'), (b'SUBMITTED', b'SUBMITTED'), (b'REJECTED', b'REJECTED'), (b'ACCEPTED', b'ACCEPTED'), (b'CANCELLED', b'CANCELLED'), (b'BOOKED', b'BOOKED')]),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_customer_status',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Quote Customer Status', choices=[(b'VIEWED', b'VIEWED'), (b'QUOTED', b'QUOTED'), (b'EXPIRED', b'EXPIRED'), (b'INPROGRESS', b'INPROGRESS'), (b'SUBMITTED', b'SUBMITTED'), (b'REJECTED', b'REJECTED'), (b'ACCEPTED', b'ACCEPTED'), (b'CANCELLED', b'CANCELLED'), (b'BOOKED', b'BOOKED')]),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_request_status',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'Quote Status', choices=[(b'OPEN', b'OPEN'), (b'CLOSE', b'CLOSE')]),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_request_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 23, 6, 21, 12, 618037), null=True, verbose_name=b'Update Date', blank=True),
        ),
    ]
