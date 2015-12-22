# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0038_auto_20151019_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuotationResponse',
            fields=[
                ('quotation_id', models.AutoField(serialize=False, primary_key=True)),
                ('rate', models.FloatField(default=0.0, null=True, verbose_name=b'Rate Per Night', blank=True)),
                ('amount', models.FloatField(default=0.0, null=True, verbose_name=b'Total Amount', blank=True)),
                ('tax_amount', models.FloatField(default=0.0, null=True, verbose_name=b'Tax Amount', blank=True)),
                ('total_quote_amt', models.FloatField(default=0.0, null=True, verbose_name=b'Total Quotation Amount', blank=True)),
                ('quote_date', models.DateField(null=True, verbose_name=b'Quatation Date', blank=True)),
                ('created_date', models.DateTimeField(null=True, verbose_name=b'Created Date', blank=True)),
                ('updated_date', models.DateTimeField(default=datetime.datetime(2015, 10, 19, 9, 59, 23, 641289), null=True, verbose_name=b'Update Date', blank=True)),
                ('created_by', models.CharField(max_length=70, null=True, verbose_name=b'Created By', blank=True)),
                ('quotation_status', models.CharField(max_length=20, null=True, verbose_name=b'Quatation Status')),
                ('viewed_by_customer', models.BooleanField(default=False, verbose_name=b'Viewed By Customer')),
                ('action', models.CharField(max_length=100, verbose_name=b'Action', blank=True)),
                ('property_id', models.ForeignKey(related_name='requested_property', to='CorpRoomApp.Property')),
            ],
        ),
        migrations.CreateModel(
            name='QuoteRequest',
            fields=[
                ('quote_request_id', models.AutoField(serialize=False, primary_key=True)),
                ('quote_request_uid', models.CharField(max_length=30, null=True, verbose_name=b'Quote Unique ID', blank=True)),
                ('quote_category', models.CharField(max_length=30, null=True, verbose_name=b'Quote Category', blank=True)),
                ('quote_sub_category', models.CharField(max_length=30, null=True, verbose_name=b'Quote Category', blank=True)),
                ('quote_start_date', models.DateField(null=True, verbose_name=b'Start Date', blank=True)),
                ('quote_end_date', models.DateField(null=True, verbose_name=b'Start Date', blank=True)),
                ('quote_city', models.CharField(max_length=30, null=True, verbose_name=b'Target City', blank=True)),
                ('quote_location', models.CharField(max_length=70, null=True, verbose_name=b'Quote Category', blank=True)),
                ('quote_lowest_price', models.FloatField(default=0.0, null=True, verbose_name=b'Range Min Price', blank=True)),
                ('quote_highest_price', models.FloatField(default=0.0, null=True, verbose_name=b'Range Min Price', blank=True)),
                ('quote_no_of_guest', models.IntegerField(default=0, verbose_name=b'Number Of Guest', blank=True)),
                ('quote_no_of_room', models.IntegerField(default=0, verbose_name=b'Number Of Guest', blank=True)),
                ('quote_request_creation_date', models.DateTimeField(null=True, verbose_name=b'Created Date', blank=True)),
                ('quote_request_update_date', models.DateTimeField(default=datetime.datetime(2015, 10, 19, 9, 59, 23, 640326), null=True, verbose_name=b'Update Date', blank=True)),
                ('quote_remark', models.CharField(max_length=250, null=True, verbose_name=b'Quote Remark', blank=True)),
                ('quote_admin_status', models.CharField(max_length=20, null=True, verbose_name=b'Quote ADMIN Status', blank=True)),
                ('quote_customer_status', models.CharField(max_length=20, null=True, verbose_name=b'Quote Customer Status', blank=True)),
                ('customer_id', models.ForeignKey(related_name='customer_request', to='CorpRoomApp.Property')),
            ],
        ),
        migrations.AddField(
            model_name='quotationresponse',
            name='request_id',
            field=models.ForeignKey(related_name='qoatation_response', to='quoteapp.QuoteRequest'),
        ),
    ]
