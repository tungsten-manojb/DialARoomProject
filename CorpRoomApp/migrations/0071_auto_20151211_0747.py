# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0070_auto_20151211_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 194836)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 194291)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 180800)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 198730)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 183718)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 191603)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 197800)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 197944), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 199730), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 193390), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='promotion_code',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 196175)),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 185644)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 186812)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 182801)),
        ),
        migrations.AlterField(
            model_name='userbookingstatistictrack',
            name='current_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 201192), verbose_name=b'Current Time Stamp'),
        ),
        migrations.AlterField(
            model_name='usertrackingactivity',
            name='session_out_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 47, 20, 200639), verbose_name=b'Session Out Time'),
        ),
    ]
