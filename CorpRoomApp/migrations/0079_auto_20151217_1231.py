# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0078_auto_20151216_0445'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingGuest',
            fields=[
                ('guest_booking_id', models.AutoField(serialize=False, primary_key=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 805558))),
            ],
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 804057)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 803647)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 789471)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 808696)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 792709)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 800932)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 807745)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 808008), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 809364), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 802746), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='promotion_code',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 806104)),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_actual_name',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Property Actual Name'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_description',
            field=models.TextField(default=b'', verbose_name=b'Property Description'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_display_name',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Property Display Name'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_documents',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_facility',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_images',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 794702)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 795930)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 791744)),
        ),
        migrations.AlterField(
            model_name='userbookingstatistictrack',
            name='current_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 810839), verbose_name=b'Current Time Stamp'),
        ),
        migrations.AlterField(
            model_name='usertrackingactivity',
            name='session_out_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 810270), verbose_name=b'Session Out Time'),
        ),
        migrations.AddField(
            model_name='bookingguest',
            name='booking_id',
            field=models.ForeignKey(related_name='all_guest', blank=True, to='CorpRoomApp.Booking'),
        ),
        migrations.AddField(
            model_name='bookingguest',
            name='guest_id',
            field=models.ForeignKey(related_name='booked_guest', blank=True, to='CorpRoomApp.Guest'),
        ),
    ]
