# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0008_auto_20150925_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='booking_amount',
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 13, 19, 59, 820120)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 13, 19, 59, 819494)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_estimated_no_of_night_stay',
            field=models.PositiveIntegerField(null=True, verbose_name=b'Estimated Nights', blank=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='payment_transaction_id',
            field=models.ForeignKey(related_name='BookingPayment', verbose_name=b'PaymentTransaction', blank=True, to='CorpRoomApp.PaymentTransaction', null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 13, 19, 59, 802307)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 13, 19, 59, 806809)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 13, 19, 59, 815739)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 9, 25, 13, 19, 59, 825803)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 13, 19, 59, 826052), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 13, 19, 59, 817836), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 13, 19, 59, 809462)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 13, 19, 59, 811165)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 13, 19, 59, 805430)),
        ),
    ]
