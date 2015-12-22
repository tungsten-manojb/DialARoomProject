# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0068_auto_20151211_0739'),
        ('quoteapp', '0030_auto_20151211_0737'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRequestStatisticTrack',
            fields=[
                ('user_request_statistic_track_id', models.AutoField(serialize=False, primary_key=True)),
                ('booking_path', models.CharField(max_length=100, verbose_name=b'Booking Path')),
                ('count', models.PositiveIntegerField(default=1)),
                ('current_timestamp', models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 39, 24, 187102), verbose_name=b'Current Time Stamp')),
                ('request_date', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='quotationresponse',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 39, 24, 185492), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_request_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 39, 24, 184097), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='requestedproperty',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 39, 24, 186462), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AddField(
            model_name='userrequeststatistictrack',
            name='request_id',
            field=models.ForeignKey(verbose_name=b'Quotation Request', to='quoteapp.QuoteRequest', null=True),
        ),
        migrations.AddField(
            model_name='userrequeststatistictrack',
            name='user_id',
            field=models.ForeignKey(verbose_name=b'Customer Name', blank=True, to='CorpRoomApp.Customer', null=True),
        ),
    ]
