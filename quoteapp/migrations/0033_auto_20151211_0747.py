# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0032_auto_20151211_0743'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userrequeststatistictrack',
            old_name='booking_path',
            new_name='request_path',
        ),
        migrations.AlterField(
            model_name='quotationresponse',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 46, 58, 775276), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_request_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 46, 58, 774107), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='requestedproperty',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 46, 58, 776131), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='userrequeststatistictrack',
            name='current_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 11, 7, 46, 58, 776728), verbose_name=b'Current Time Stamp'),
        ),
    ]
