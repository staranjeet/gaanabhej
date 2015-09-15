from django.db import models
from django.contrib.auth.models	import User

# Create your models here.
class SongDetails(models.Model):

	url 		= models.URLField(primary_key=True,max_length=1024)
	name		= models.CharField(max_length=255)
	artist		= models.CharField(max_length=255)
	duration	= models.CharField(max_length=255)
	likes		= models.CharField(max_length=50)
	views		= models.CharField(max_length=50)
	dislikes	= models.CharField(max_length=50)

	class Meta:
		verbose_name_plural = 'Song Details'
		verbose_name 		= 'Song Details'
		db_table 			= 'song_details'

	def __str__(self):
		return self.url

	def __unicode__(self):
		return self.url

class SuggestedSongs(models.Model):

	id 			= models.AutoField(primary_key=True)
	suggestedTo	= models.ForeignKey(User,db_column='suggested_to',related_name='suggested_to_user')
	suggestedBy	= models.ForeignKey(User,db_column='suggested_by',related_name='suggested_by_user')
	song 		= models.ForeignKey(SongDetails)
	isSeen		= models.BooleanField(default=False,db_column='is_seen')

	class Meta:
		verbose_name_plural = 'Songs Suggested'
		verbose_name 		= 'Song Suggested'
		db_table			= 'suggested_songs'

	def __str__(self):
		return self.id

	def __unicode__(self):
		return self.id