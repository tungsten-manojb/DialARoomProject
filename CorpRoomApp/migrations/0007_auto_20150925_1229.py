# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0006_auto_20150922_0555'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_amount',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 12, 29, 45, 573751)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 12, 29, 45, 573372)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='payment_method',
            field=models.CharField(max_length=150, null=True, verbose_name=b'Payment Method', choices=[(b'ONLINE', b'ON-LINE'), (b'ONCHECKOUT', b'ON-CHECK-OUT')]),
        ),
        migrations.AlterField(
            model_name='booking',
            name='payment_status',
            field=models.IntegerField(default=0, verbose_name=b'Payement Status', choices=[(1, b'PAID'), (0, b'UNPAID')]),
        ),
        migrations.AlterField(
            model_name='booking',
            name='property_id',
            field=models.ForeignKey(related_name='PropertyBookings', verbose_name=b'PROPERTY Name', to='CorpRoomApp.Property', null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 12, 29, 45, 559989)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 12, 29, 45, 563017)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 12, 29, 45, 570819)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 9, 25, 12, 29, 45, 576801)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 12, 29, 45, 576924), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_status',
            field=models.CharField(default=b'U', max_length=3, verbose_name=b'Status', choices=[(1, b'PAID'), (0, b'UNPAID')]),
        ),
        migrations.AlterField(
            model_name='location',
            name='location_name',
            field=models.CharField(max_length=150, null=True, verbose_name=b'Location'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 12, 29, 45, 572495), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='property',
            name='existing_occupacy',
            field=models.CharField(max_length=30, null=True, verbose_name=b'Existing Occupancy'),
        ),
        migrations.AlterField(
            model_name='property',
            name='latitude',
            field=models.CharField(default=b'0', max_length=20, verbose_name=b'Latitude'),
        ),
        migrations.AlterField(
            model_name='property',
            name='longitude',
            field=models.CharField(default=b'0', max_length=20, verbose_name=b'Longitude'),
        ),
        migrations.AlterField(
            model_name='property',
            name='no_of_person_allowed_per_room',
            field=models.IntegerField(default=2, null=True, verbose_name=b'No Of Person Per Room'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_availability_status',
            field=models.BooleanField(verbose_name=b'Property Availability', choices=[(True, b'AVAILABLE'), (False, b'NOT AVAILABLE')]),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 12, 29, 45, 564704)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 12, 29, 45, 565918)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 25, 12, 29, 45, 562037)),
        ),
    ]
