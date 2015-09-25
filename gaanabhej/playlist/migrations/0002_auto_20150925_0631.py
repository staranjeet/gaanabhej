# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestedsongs',
            name='suggestedTo',
            field=models.ForeignKey(related_query_name=b'touser', related_name='suggested_to_user', db_column=b'suggested_to', to=settings.AUTH_USER_MODEL),
        ),
    ]
