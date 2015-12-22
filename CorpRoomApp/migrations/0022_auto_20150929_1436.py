# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0021_auto_20150929_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='location',
        ),
        migrations.AddField(
            model_name='property',
            name='property_city',
            field=models.CharField(max_length=50, null=True, verbose_name=b'City'),
        ),
        migrations.AddField(
            model_name='property',
            name='property_country',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Country'),
        ),
        migrations.AddField(
            model_name='property',
            name='property_location',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Location'),
        ),
        migrations.AddField(
            model_name='property',
            name='property_state',
            field=models.CharField(max_length=50, null=True, verbose_name=b'State'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 29, 14, 36, 8, 817253)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 29, 14, 36, 8, 816873)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 29, 14, 36, 8, 803893)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 29, 14, 36, 8, 821116)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 29, 14, 36, 8, 806702)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 29, 14, 36, 8, 814331)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 9, 29, 14, 36, 8, 820339)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 29, 14, 36, 8, 820463), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 29, 14, 36, 8, 821751), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 29, 14, 36, 8, 815991), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 29, 14, 36, 8, 808469)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 29, 14, 36, 8, 809591)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 29, 14, 36, 8, 805817)),
        ),
    ]
