# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0039_auto_20151019_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 88605)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 88231)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 75133)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 92503)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_company_id',
            field=models.ForeignKey(related_name='customerCompany', verbose_name=b'Company Name', blank=True, to='CorpRoomApp.Company', null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 77912)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 85679)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 91696)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 91838), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 93283), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 87356), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='promotion_code',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 90043)),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 79762)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 80902)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 20, 6, 1, 3, 77042)),
        ),
    ]
