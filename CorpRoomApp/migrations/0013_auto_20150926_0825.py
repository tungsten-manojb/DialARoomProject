# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CorpRoomApp', '0012_auto_20150926_0632'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorporateTransaction',
            fields=[
                ('transaction_id', models.AutoField(serialize=False, primary_key=True)),
                ('invoice_id', models.CharField(max_length=50, null=True, verbose_name=b'Invoice', blank=True)),
                ('transaction_date', models.DateField(default=datetime.datetime(2015, 9, 26, 8, 25, 44, 341157))),
                ('transaction_amount', models.FloatField(default=0.0, null=True, verbose_name=b'Transaction Amount')),
                ('transaction_type', models.IntegerField(null=True, verbose_name=b'Transaction Type', choices=[(0, b'INVOICE'), (1, b'PAYMENT'), (2, b'DEPOSIT')])),
                ('corporate_id', models.ForeignKey(related_name='corporate_id', verbose_name=b'Corporate Details', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 8, 25, 44, 336080)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 8, 25, 44, 335655)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 8, 25, 44, 322027)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 8, 25, 44, 325055)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 8, 25, 44, 333211)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 9, 26, 8, 25, 44, 339798)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 8, 25, 44, 339915), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 8, 25, 44, 334772), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 8, 25, 44, 326668)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 8, 25, 44, 328219)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 8, 25, 44, 324279)),
        ),
    ]
