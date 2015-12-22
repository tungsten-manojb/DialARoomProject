# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('CorpRoomApp', '0005_auto_20150922_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 55, 20, 11963)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 55, 20, 11583)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 55, 19, 997639)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 55, 20, 517)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='relationship_manager_id',
            field=models.ForeignKey(related_name='relationManager', verbose_name=b'RelationShipManager', blank=True, to='CorpRoomApp.RelationShipManager', null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 55, 20, 8976)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 5, 55, 20, 14971)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 55, 20, 15093), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 55, 20, 10689), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_owner_id',
            field=models.ForeignKey(related_name='ProperyOwnerID', verbose_name=b'Owner Name', blank=True, to='CorpRoomApp.Customer', null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 55, 20, 2142)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 55, 20, 3753)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 5, 55, 19, 999613)),
        ),
    ]
