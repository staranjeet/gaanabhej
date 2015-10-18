from django	import forms
from django.contrib.auth.models import User
from django.db.models import Q

from playlist.models import (
							SongDetails,
							MySongModel)

def getUser(userid):
	userList = User.objects.filter(~Q(id=userid))
	selectUserList = [(eachUser.id,eachUser.username) for eachUser in userList]
	selectUserList.insert(0,("","Select User"))
	return selectUserList

def getSongs(userid):
	songsList = MySongModel.objects.filter(owner=userid)
	songs =[(eachSong.song.url, eachSong.song.name) for eachSong in songsList]
	songs.insert(0, ("","Select Song"))
	return songs

class SuggestSongForm(forms.Form):

	def __init__(self,*args,**kwargs):
		self.user = kwargs.pop('user',None)
		super(SuggestSongForm,self).__init__(*args,**kwargs)
		self.fields['suggestedTo'] = forms.ChoiceField(choices=getUser(self.user.id),
			required=True,
			label		= 'Suggested To User',
			help_text 	= 'Suggested to',
			widget	= forms.Select(attrs={'class' : 'form-control', 
							'placeholder' : 'I would like to suggest to','style':'width:100%;'}
			))
		self.fields['songName'] = forms.ChoiceField(choices=getSongs(self.user.id),
			help_text='Name of the song to be suggested',
			required=True,
			widget=forms.Select(attrs={'class' : 'form-control',
				'placeholder' : 'Your suggestion here'}
			))

	
class AddSongToPlayListForm(forms.ModelForm):

	class Meta:
		model = SongDetails
		fields = ('url', )

	def __init__(self, *args, **kwargs):
		super(AddSongToPlayListForm, self).__init__(*args, **kwargs)
		self.fields['url'].widget.attrs.update({
			'class' : 'form-control',
			'placeholder' : 'Paste the Youtube url here'
			})


