# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0003_auto_20150918_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='created_by',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='updated_by',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 45, 43, 824034)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 45, 43, 823658)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_status',
            field=models.IntegerField(default=0, verbose_name=b'Status', choices=[(0, b'AVAILABLE'), (1, b'OPEN'), (2, b'BOOKED'), (3, b'CANCELLED'), (4, b'COMPLETED')]),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 45, 43, 810545)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_address_line',
            field=models.CharField(default=b'', max_length=150, null=True, verbose_name=b'Address Line '),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_city',
            field=models.CharField(default=b'', max_length=50, null=True, verbose_name=b'City '),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_contact_no',
            field=models.CharField(default=b'', max_length=50, null=True, verbose_name=b'Contact Number'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_email',
            field=models.CharField(default=b'', max_length=50, null=True, verbose_name=b'Email Id '),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_first_name',
            field=models.CharField(default=b'', max_length=50, null=True, verbose_name=b'First Name '),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_last_name',
            field=models.CharField(default=b'', max_length=50, null=True, verbose_name=b'Last Name '),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 45, 43, 813432)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='sign_up_device',
            field=models.CharField(default=b'', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='sign_up_source',
            field=models.CharField(default=b'', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 45, 43, 821103)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 5, 45, 43, 827081)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 45, 43, 827201), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 45, 43, 822770), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_documents',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_facility',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_images',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_status',
            field=models.IntegerField(default=0, null=True, verbose_name=b'Status', choices=[(0, b'AVAILABLE'), (1, b'OPEN'), (2, b'BOOKED'), (3, b'CANCELLED'), (4, b'COMPLETED')]),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 45, 43, 815086)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='no_of_occupant_allowed',
            field=models.IntegerField(default=0, verbose_name=b'Status', choices=[(0, b'AVAILABLE'), (1, b'OPEN'), (2, b'BOOKED'), (3, b'CANCELLED'), (4, b'COMPLETED')]),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_status',
            field=models.IntegerField(default=0, verbose_name=b'Status', choices=[(0, b'AVAILABLE'), (1, b'OPEN'), (2, b'BOOKED'), (3, b'CANCELLED'), (4, b'COMPLETED')]),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_type',
            field=models.CharField(default=0, max_length=12, verbose_name=b'Room Type', choices=[(b'Single', b'Single Bed'), (b'Double', b'Double Bed')]),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 45, 43, 816316)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 45, 43, 812528)),
        ),
    ]
