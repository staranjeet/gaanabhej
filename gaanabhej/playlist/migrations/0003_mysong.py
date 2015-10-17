# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('playlist', '0002_auto_20150925_0631'),
    ]

    operations = [
        migrations.CreateModel(
            name='MySongModel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('owner', models.ForeignKey(related_name='adding_user', db_column=b'listener', to=settings.AUTH_USER_MODEL)),
                ('song', models.ForeignKey(related_name='my_song', db_column=b'song_added', to='playlist.SongDetails')),
            ],
            options={
                'db_table': 'my_song',
                'verbose_name': 'MY Song',
                'verbose_name_plural': 'My Songs',
            },
        ),
    ]
