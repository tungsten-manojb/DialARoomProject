# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0061_auto_20151210_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBookingStatisticTrack',
            fields=[
                ('user_booking_statistic_track_id', models.AutoField(serialize=False, primary_key=True)),
                ('booking_path', models.CharField(max_length=100, verbose_name=b'Booking Path')),
                ('count', models.PositiveIntegerField(default=1)),
                ('current_timestamp', models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 382495), verbose_name=b'Current Time Stamp')),
                ('booking_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='UserRequestStatisticTrack',
            fields=[
                ('user_request_statistic_track_id', models.AutoField(serialize=False, primary_key=True)),
                ('booking_path', models.CharField(max_length=100, verbose_name=b'Booking Path')),
                ('count', models.PositiveIntegerField(default=1)),
                ('current_timestamp', models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 383050), verbose_name=b'Current Time Stamp')),
                ('request_date', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 376389)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 375925)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 363039)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 380293)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 364787)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 373330)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 379293)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 379412), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 381034), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 375041), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='promotion_code',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 377725)),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 366557)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 368477)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 363995)),
        ),
        migrations.AlterField(
            model_name='usertrackingactivity',
            name='session_out_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 11, 27, 381948), verbose_name=b'Session Out Time'),
        ),
        migrations.AddField(
            model_name='userrequeststatistictrack',
            name='user_id',
            field=models.ForeignKey(verbose_name=b'Customer Name', blank=True, to='CorpRoomApp.Customer', null=True),
        ),
        migrations.AddField(
            model_name='userbookingstatistictrack',
            name='user_id',
            field=models.ForeignKey(verbose_name=b'Customer Name', blank=True, to='CorpRoomApp.Customer', null=True),
        ),
    ]
