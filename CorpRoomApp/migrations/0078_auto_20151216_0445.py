# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0077_auto_20151214_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 628157)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 627714)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 614259)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 632233)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 617050)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 625074)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 631323)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 631459), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 632889), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 626818), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='promotion_code',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 629639)),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_documents',
            field=models.TextField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_facility',
            field=models.TextField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_images',
            field=models.TextField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 618973)),
        ),
        migrations.AlterField(
            model_name='property',
            name='remark',
            field=models.TextField(null=True, verbose_name=b'Remark'),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 620243)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 616188)),
        ),
        migrations.AlterField(
            model_name='userbookingstatistictrack',
            name='current_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 634349), verbose_name=b'Current Time Stamp'),
        ),
        migrations.AlterField(
            model_name='usertrackingactivity',
            name='session_out_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 4, 45, 36, 633784), verbose_name=b'Session Out Time'),
        ),
    ]
