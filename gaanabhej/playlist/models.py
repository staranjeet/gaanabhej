from django.db import models
from django.contrib.auth.models	import User

# Create your models here.
class SongDetails(models.Model):


	# songId 		= models.AutoField(primary_key=True)
	url 		= models.URLField(max_length=1024,primary_key=True)
	name		= models.CharField(max_length=255)
	artist		= models.CharField(max_length=255)
	duration	= models.CharField(max_length=255)
	likes		= models.CharField(max_length=50,verbose_name='Likes')
	views		= models.CharField(max_length=50,verbose_name='Views')
	dislikes	= models.CharField(max_length=50,verbose_name='DisLikes')

	class Meta:
		verbose_name_plural = 'Song Details'
		verbose_name 		= 'Song Details'
		db_table 			= 'song_details'

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name

class SuggestedSongs(models.Model):

	id 			= models.AutoField(primary_key=True)
	suggestedTo	= models.ForeignKey(User,db_column='suggested_to',related_name='suggested_to_user',related_query_name='touser')
	suggestedBy	= models.ForeignKey(User,db_column='suggested_by',related_name='suggested_by_user')
	song 		= models.ForeignKey(SongDetails)
	isSeen		= models.BooleanField(default=False,db_column='is_seen',verbose_name='Listened by user?')
	score 		= models.IntegerField(default=0,db_column='score')

	class Meta:
		verbose_name_plural = 'Songs Suggested'
		verbose_name 		= 'Song Suggested'
		db_table			= 'suggested_songs'

	def __str__(self):
		return str(self.id)

	def __unicode__(self):
		return str(self.id)

# class ExtendedUser(models.Model):
# 	pass

class MySongModel(models.Model):

	id = models.AutoField(primary_key=True)
	song = models.ForeignKey(SongDetails, db_column='song_added', related_name='my_song')
	owner = models.ForeignKey(User, db_column='listener', related_name='adding_user')

	class Meta:
		verbose_name = 'My Song'
		verbose_name_plural = 'My Songs'
		db_table = 'my_song'

	def __unicode__(self):
		return '{} : {}'.format(self.owner.username, self.song.name)
