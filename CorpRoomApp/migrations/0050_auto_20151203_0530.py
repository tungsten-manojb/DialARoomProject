# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0049_auto_20151109_0551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 3, 5, 30, 26, 449149)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 3, 5, 30, 26, 448739)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 3, 5, 30, 26, 431111)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 3, 5, 30, 26, 456923)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_address_line',
            field=models.CharField(default=b'', max_length=250, verbose_name=b'Address Line '),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_age',
            field=models.PositiveIntegerField(default=0, verbose_name=b'Age'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_city',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'City '),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_contact_no',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Contact Number'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_country',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Country '),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_email',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Email Id '),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_first_name',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'First Name '),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_gender',
            field=models.CharField(default=b'M', max_length=20, verbose_name=b'Gender', choices=[(b'M', b'MALE'), (b'F', b'FEMALE')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_last_name',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Last Name '),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_pincode',
            field=models.PositiveIntegerField(default=0, verbose_name=b'Pincode'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_state',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'State '),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 3, 5, 30, 26, 432871)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='sign_up_device',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='sign_up_source',
            field=models.CharField(default=b'', max_length=15),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 3, 5, 30, 26, 446070)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 12, 3, 5, 30, 26, 455047)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 3, 5, 30, 26, 455288), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 3, 5, 30, 26, 458305), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 3, 5, 30, 26, 447792), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='property_booking_id',
            field=models.CharField(max_length=250, null=True, verbose_name=b'property_booking_id', blank=True),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='udf6',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Invoices', blank=True),
        ),
        migrations.AlterField(
            model_name='promotion_code',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 3, 5, 30, 26, 451775)),
        ),
        migrations.AlterField(
            model_name='property',
            name='created_by',
            field=models.CharField(default=b'', max_length=40),
        ),
        migrations.AlterField(
            model_name='property',
            name='no_of_person_allowed_per_room',
            field=models.IntegerField(default=2, verbose_name=b'No Of Person Per Room'),
        ),
        migrations.AlterField(
            model_name='property',
            name='number_of_rooms',
            field=models.PositiveIntegerField(default=0, verbose_name=b'Number Of Rooms '),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_address',
            field=models.CharField(default=b'', max_length=200, verbose_name=b'Address Line'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_city',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'City'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_country',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Country'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_documents',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_facility',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_images',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_location',
            field=models.CharField(default=b'', max_length=100, verbose_name=b'Location'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_pincode',
            field=models.CharField(default=b'', max_length=10, verbose_name=b'Pincode'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_state',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'State'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 3, 5, 30, 26, 435529)),
        ),
        migrations.AlterField(
            model_name='property',
            name='star_category',
            field=models.IntegerField(default=0, verbose_name=b'Star Category'),
        ),
        migrations.AlterField(
            model_name='property',
            name='updated_by',
            field=models.CharField(default=b'', max_length=40),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 3, 5, 30, 26, 437843)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 3, 5, 30, 26, 431979)),
        ),
    ]
