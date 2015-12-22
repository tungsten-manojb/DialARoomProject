# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0018_auto_20150927_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('mailing_list_id', models.AutoField(serialize=False, primary_key=True)),
                ('mail_id', models.CharField(max_length=50, null=True, verbose_name=b'Mail ID', blank=True)),
                ('updated_date', models.DateTimeField(default=datetime.datetime(2015, 9, 28, 18, 28, 9, 820554), verbose_name=b'Requested Date Time')),
            ],
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 28, 18, 28, 9, 815595)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 28, 18, 28, 9, 815269)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 28, 18, 28, 9, 802711)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 28, 18, 28, 9, 820027)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 28, 18, 28, 9, 805528)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 28, 18, 28, 9, 812846)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 9, 28, 18, 28, 9, 819208)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 28, 18, 28, 9, 819315), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 28, 18, 28, 9, 814425), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 28, 18, 28, 9, 807087)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 28, 18, 28, 9, 808273)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 28, 18, 28, 9, 804729)),
        ),
    ]
