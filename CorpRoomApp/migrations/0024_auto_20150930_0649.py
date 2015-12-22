# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0023_auto_20150929_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 6, 49, 14, 218514)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 6, 49, 14, 218121)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='payment_status',
            field=models.CharField(default=b'0', max_length=1, verbose_name=b'Payement Status', choices=[(b'1', b'PAID'), (b'0', b'UNPAID')]),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 6, 49, 14, 204685)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 30, 6, 49, 14, 222535)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 6, 49, 14, 207728)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 6, 49, 14, 215447)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='booking_id',
            field=models.ForeignKey(related_name='invoicebooking', verbose_name=b'Booking ID', to='CorpRoomApp.Booking', null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 9, 30, 6, 49, 14, 221738)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 6, 49, 14, 221877), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_status',
            field=models.CharField(default=b'0', max_length=1, verbose_name=b'Status', choices=[(b'1', b'PAID'), (b'0', b'UNPAID')]),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 6, 49, 14, 223158), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 6, 49, 14, 217164), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 6, 49, 14, 209535)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 6, 49, 14, 210701)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 30, 6, 49, 14, 206842)),
        ),
    ]
