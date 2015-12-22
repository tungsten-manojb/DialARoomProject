# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0011_auto_20151102_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationresponse',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 756677), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='quote_request_update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 755644), null=True, verbose_name=b'Update Date', blank=True),
        ),
        migrations.AlterField(
            model_name='requestedproperty',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 9, 5, 51, 57, 757510), null=True, verbose_name=b'Update Date', blank=True),
        ),
    ]
