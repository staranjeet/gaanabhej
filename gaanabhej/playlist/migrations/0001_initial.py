# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SongDetails',
            fields=[
                ('url', models.URLField(max_length=1024, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('duration', models.CharField(max_length=255)),
                ('likes', models.CharField(max_length=50, verbose_name=b'Likes')),
                ('views', models.CharField(max_length=50, verbose_name=b'Views')),
                ('dislikes', models.CharField(max_length=50, verbose_name=b'DisLikes')),
            ],
            options={
                'db_table': 'song_details',
                'verbose_name': 'Song Details',
                'verbose_name_plural': 'Song Details',
            },
        ),
        migrations.CreateModel(
            name='SuggestedSongs',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('isSeen', models.BooleanField(default=False, verbose_name=b'Listened by user?', db_column=b'is_seen')),
                ('score', models.IntegerField(default=0, db_column=b'score')),
                ('song', models.ForeignKey(to='playlist.SongDetails')),
                ('suggestedBy', models.ForeignKey(related_name='suggested_by_user', db_column=b'suggested_by', to=settings.AUTH_USER_MODEL)),
                ('suggestedTo', models.ForeignKey(related_name='suggested_to_user', db_column=b'suggested_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'suggested_songs',
                'verbose_name': 'Song Suggested',
                'verbose_name_plural': 'Songs Suggested',
            },
        ),
    ]
