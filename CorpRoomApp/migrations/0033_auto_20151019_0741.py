# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0032_auto_20151008_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 7, 41, 18, 930147)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 7, 41, 18, 929765)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 7, 41, 18, 916596)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='cheque_bank_branch',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Bank Name & Branch', blank=True),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 10, 19, 7, 41, 18, 934020)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_method',
            field=models.CharField(max_length=10, null=True, verbose_name=b'Method', choices=[(b'CASH', b'CASH'), (b'CHEQUE', b'CHEQUE')]),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_type',
            field=models.IntegerField(null=True, verbose_name=b'Transaction Type', choices=[(0, b'DEPOSIT'), (1, b'INVOICE')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 7, 41, 18, 919402)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 7, 41, 18, 927183)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 10, 19, 7, 41, 18, 933216)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 7, 41, 18, 933358), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 7, 41, 18, 934799), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 7, 41, 18, 928880), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='promotion_code',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 7, 41, 18, 931573)),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 7, 41, 18, 921249)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 7, 41, 18, 922387)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 7, 41, 18, 918473)),
        ),
    ]
