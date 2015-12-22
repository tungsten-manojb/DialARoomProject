# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0025_auto_20150930_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 9, 0, 57, 515995)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 9, 0, 57, 515620)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 9, 0, 57, 502504)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 10, 7, 9, 0, 57, 519863)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 9, 0, 57, 505229)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 9, 0, 57, 513070)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 10, 7, 9, 0, 57, 519061)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 9, 0, 57, 519205), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 9, 0, 57, 520483), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 9, 0, 57, 514745), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 9, 0, 57, 507028)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 9, 0, 57, 508150)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_contactno',
            field=models.CharField(max_length=40, null=True, verbose_name=b'Contact  No'),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_email',
            field=models.CharField(max_length=40, null=True, verbose_name=b'Email Id'),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_first_name',
            field=models.CharField(max_length=40, null=True, verbose_name=b'First Name'),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_last_name',
            field=models.CharField(max_length=40, null=True, verbose_name=b'Last Name'),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_status',
            field=models.IntegerField(default=1, verbose_name=b'Company Status', choices=[(1, b'ACTIVE'), (0, b'IN-ACTIVE')]),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_unique_id',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Manager Id'),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 7, 9, 0, 57, 504370)),
        ),
    ]
