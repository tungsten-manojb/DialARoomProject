# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0044_auto_20151031_0700'),
        ('quoteapp', '0006_auto_20151028_0654'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestedProperty',
            fields=[
                ('requested_property_id', models.AutoField(serialize=False, primary_key=True)),
                ('created_date', models.DateTimeField(null=True, verbose_name=b'Created Date', blank=True)),
                ('updated_date', models.DateTimeField(default=datetime.datetime(2015, 10, 31, 7, 0, 43, 113036), null=True, verbose_name=b'Update Date', blank=True)),
                ('created_by', models.CharField(max_length=70, null=True, verbose_name=b'Created By', blank=True)),
                ('property_id', models.ForeignKey(related_name='r_property', to='CorpRoomApp.Property')),
            ],
        ),
        migrations.AlterField(
            model_name='quotationresponse',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 31, 7, 0, 43, 112037), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_request_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 31, 7, 0, 43, 110815), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AddField(
            model_name='requestedproperty',
            name='quote_request_id',
            field=models.ForeignKey(related_name='requested_property', to='quoteapp.QuoteRequest'),
        ),
    ]
