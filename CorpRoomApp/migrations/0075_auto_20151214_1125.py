# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0074_auto_20151214_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 497322)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 496771)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 480151)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 501272)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 483629)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 493608)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 500337)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 500478), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 501951), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 495793), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='promotion_code',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 498707)),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 485706)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 486990)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 482562)),
        ),
        migrations.AlterField(
            model_name='userbookingstatistictrack',
            name='current_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 503407), verbose_name=b'Current Time Stamp'),
        ),
        migrations.AlterField(
            model_name='usertrackingactivity',
            name='session_out_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 38, 502854), verbose_name=b'Session Out Time'),
        ),
    ]
