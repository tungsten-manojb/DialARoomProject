# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0048_auto_20151102_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 733672)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 733266)),
        ),
        migrations.AlterField(
            model_name='city',
            name='city_name',
            field=models.CharField(max_length=30, null=True, verbose_name=b'Location'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 720086)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 737706)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 722909)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 730710)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 736802)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 736937), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 738399), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 732388), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='promotion_code',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 735153)),
        ),
        migrations.AlterField(
            model_name='property',
            name='contact_person_email_id',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Contact Person Email'),
        ),
        migrations.AlterField(
            model_name='property',
            name='contact_person_phone_no',
            field=models.CharField(max_length=15, null=True, verbose_name=b'Contact Person Phone'),
        ),
        migrations.AlterField(
            model_name='property',
            name='latitude',
            field=models.FloatField(default=0.0, max_length=20, verbose_name=b'Latitude'),
        ),
        migrations.AlterField(
            model_name='property',
            name='longitude',
            field=models.FloatField(default=0.0, max_length=20, verbose_name=b'Longitude'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 724753)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 725940)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 722051)),
        ),
    ]
