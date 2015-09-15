# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestedsongs',
            name='score',
            field=models.IntegerField(default=0, db_column=b'score'),
        ),
    ]
