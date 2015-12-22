# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0024_auto_20150930_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='extra_charge_details',
            field=models.CharField(default=b'', max_length=100, verbose_name=b'Extra Charge Details'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 9, 10, 37, 952767)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 9, 10, 37, 952381)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 9, 10, 37, 938957)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 30, 9, 10, 37, 956669)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 9, 10, 37, 941740)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 9, 10, 37, 949680)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 9, 30, 9, 10, 37, 955869)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 9, 10, 37, 956012), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 9, 10, 37, 957312), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 9, 10, 37, 951477), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 9, 10, 37, 943557)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 9, 10, 37, 944730)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 9, 10, 37, 940891)),
        ),
    ]
