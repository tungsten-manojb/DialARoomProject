# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0079_auto_20151217_1231'),
        ('quoteapp', '0041_auto_20151216_0445'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestedproperty',
            name='property_owner_id',
            field=models.ForeignKey(related_name='owner_req_property', to='CorpRoomApp.Customer', null=True),
        ),
        migrations.AlterField(
            model_name='quotationresponse',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 831451), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_request_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 830333), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='requestedproperty',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 832432), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='userrequeststatistictrack',
            name='current_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 12, 31, 19, 833126), verbose_name=b'Current Time Stamp'),
        ),
    ]
