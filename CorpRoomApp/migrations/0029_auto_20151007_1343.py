# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0028_auto_20151007_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporatetransaction',
            name='cheque_bank',
            field=models.CharField(max_length=15, null=True, verbose_name=b'Cheque Number', blank=True),
        ),
        migrations.AddField(
            model_name='corporatetransaction',
            name='cheque_number',
            field=models.CharField(max_length=15, null=True, verbose_name=b'Cheque Number', blank=True),
        ),
        migrations.AddField(
            model_name='corporatetransaction',
            name='transaction_desc',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 13, 43, 53, 279787)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 13, 43, 53, 279400)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 13, 43, 53, 265544)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 10, 7, 13, 43, 53, 283743)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_type',
            field=models.IntegerField(null=True, verbose_name=b'Transaction Type', choices=[(0, b'CASH'), (1, b'CHEQUE')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 13, 43, 53, 268475)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 13, 43, 53, 276777)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 10, 7, 13, 43, 53, 282885)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 13, 43, 53, 283071), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 13, 43, 53, 284481), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 13, 43, 53, 278511), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 13, 43, 53, 270442)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 13, 43, 53, 271719)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 13, 43, 53, 267581)),
        ),
    ]
