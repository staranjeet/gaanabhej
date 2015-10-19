# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('playlist', '0003_mysong'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0, db_column=b'score')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'Users Profile',
            },
        ),
        migrations.AlterModelOptions(
            name='mysongmodel',
            options={'verbose_name': 'My Song', 'verbose_name_plural': 'My Songs'},
        ),
    ]
