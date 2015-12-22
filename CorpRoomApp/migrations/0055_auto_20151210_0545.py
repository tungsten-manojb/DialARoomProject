# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CorpRoomApp', '0054_auto_20151207_1337'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTrackingActivity',
            fields=[
                ('user_tracking_id', models.AutoField(serialize=False, primary_key=True)),
                ('path', models.CharField(default=b'', max_length=5000, verbose_name=b'Path Flow')),
                ('session_in_time', models.DateTimeField(verbose_name=b'Session In Time')),
                ('session_out_time', models.DateTimeField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 556946), verbose_name=b'Session Out Time')),
                ('session_id', models.CharField(max_length=100, verbose_name=b'Session ID')),
                ('aggregate_time', models.DateTimeField(null=True)),
                ('user_id', models.ForeignKey(related_name='user_track', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 551280)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 550859)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 537469)),
        ),
        migrations.AlterField(
            model_name='corporatetransaction',
            name='transaction_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 555310)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 540219)),
        ),
        migrations.AlterField(
            model_name='guest',
            name='guest_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 548173)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_datetime',
            field=models.DateField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 554399)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_generated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 554537), verbose_name=b'Invoice Generated DateTime'),
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 555970), verbose_name=b'Requested Date Time'),
        ),
        migrations.AlterField(
            model_name='paymenttransaction',
            name='booking_transaction_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 549946), verbose_name=b'Update Date'),
        ),
        migrations.AlterField(
            model_name='promotion_code',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 552744)),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 542040)),
        ),
        migrations.AlterField(
            model_name='propertyroom',
            name='room_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 543220)),
        ),
        migrations.AlterField(
            model_name='relationshipmanager',
            name='rm_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 10, 5, 45, 13, 539354)),
        ),
    ]
