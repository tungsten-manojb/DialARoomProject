# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0073_auto_20151214_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 22270)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 21738)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 8190)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 26247)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 11001)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 19066)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 25294)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 25452), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 26914), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 20823), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='promotion_code',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 23633)),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 12873)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 14193)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 10137)),
        ),
        migrations.AlterField(
            model_name='userbookingstatistictrack',
            name='current_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 28362), verbose_name=b'Current Time Stamp'),
        ),
        migrations.AlterField(
            model_name='usertrackingactivity',
            name='session_out_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 11, 25, 17, 27809), verbose_name=b'Session Out Time'),
        ),
    ]
