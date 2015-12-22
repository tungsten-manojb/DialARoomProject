# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0063_auto_20151211_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbookingstatistictrack',
            name='booking_obj',
            field=models.ForeignKey(verbose_name=b'Customer Booking', to='CorpRoomApp.Booking', null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 329868)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 329323)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 312041)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 334066)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 314968)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 326554)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 333071)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 333218), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 334753), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 328392), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='promotion_code',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 331317)),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 316767)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 318481)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 314099)),
        ),
        migrations.AlterField(
            model_name='userbookingstatistictrack',
            name='current_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 336234), verbose_name=b'Current Time Stamp'),
        ),
        migrations.AlterField(
            model_name='userrequeststatistictrack',
            name='current_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 336874), verbose_name=b'Current Time Stamp'),
        ),
        migrations.AlterField(
            model_name='usertrackingactivity',
            name='session_out_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 29, 12, 335676), verbose_name=b'Session Out Time'),
        ),
    ]
