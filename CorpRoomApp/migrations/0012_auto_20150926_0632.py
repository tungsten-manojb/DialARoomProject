# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0011_auto_20150926_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 6, 32, 33, 301951)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 6, 32, 33, 301474)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='customer_id',
            field=models.ForeignKey(related_name='customerbooking', verbose_name=b'CAM Name', to='CorpRoomApp.Customer', null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='guest_id',
            field=models.ForeignKey(related_name='guestbooking', verbose_name=b'Guests', to='CorpRoomApp.Guest', null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='property_id',
            field=models.ForeignKey(related_name='propertybooking', verbose_name=b'PROPERTY Name', to='CorpRoomApp.Property', null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='property_room_id',
            field=models.ForeignKey(related_name='roombooking', verbose_name=b'Room Number', to='CorpRoomApp.PropertyRoom', null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 6, 32, 33, 286190)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 6, 32, 33, 289742)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 6, 32, 33, 297908)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 9, 26, 6, 32, 33, 305952)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 6, 32, 33, 306114), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 6, 32, 33, 300121), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 6, 32, 33, 291532)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 6, 32, 33, 292790)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 26, 6, 32, 33, 288637)),
        ),
    ]
