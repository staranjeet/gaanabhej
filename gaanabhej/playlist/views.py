import urllib2,json
from lxml import etree

from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect

from .forms import PlayListForm
from playlist.models import SongDetails,SuggestedSongs


def convertToInt(no):
	no = no.replace(',','')
	return int(no)

class SuggestASong(ListView):

	template_name		= 'suggestasong.html'


	def get(self,request,*args,**kwargs):

		formObj			= PlayListForm(request.GET,user=request.user)
		suggestionToBeViewed = None
		# userList		= User.objects.filter(~Q(id=request.user.id))
		# selectUserList  = ()
		# for eachUser in userList:
			# print eachUser.id,eachUser.username
			# selectUserList = selectUserList + (eachUser.id,eachUser.username)
		# print selectUserList
		# formObj.fields["suggestedTo"].initial = selectUserList
		# print userList 

		# suggestedTo = User.objects.get(id=2)
		suggestedBy = request.user

		if formObj.is_valid():

			formCleaned 		= formObj.cleaned_data
			songURL				= formCleaned.get("songName",None)
			suggestedToId 		= formCleaned.get("suggestedTo",None)
			suggestedTo 		= User.objects.get(id=suggestedToId)
			print suggestedBy,suggestedTo

			if songURL is not None:
				print songURL
				page			= urllib2.urlopen(songURL).read()
				x	 			= etree.HTML(page)
				title			= x.xpath('//title/text()')[0]
				views			= convertToInt(x.xpath('//div[@class="watch-view-count"]/text()')[0])
				likes			= convertToInt(x.xpath('//button[@title="Unlike"]/span[@class="yt-uix-button-content"]/text()')[0])
				dislikes		= convertToInt(x.xpath('//button[@title="I dislike this"]/span[@class="yt-uix-button-content"]/text()')[0])
				# duration 		= x.xpath('//span[@class="video-time"]/text()')
				print title,views,likes,dislikes,len(title)
				newsong = SongDetails(
					url=songURL,name=title,views=views,
					dislikes=dislikes,likes=likes
					)
				newsong.save()

				

				suggestion = SuggestedSongs(suggestedTo=suggestedTo,
					suggestedBy=suggestedBy,song=newsong,isSeen=False)
				suggestion.save()

		# suggestionToBeViewed = SuggestedSongs.objects.filter(suggestedTo=suggestedBy.id,isSeen=False)
		# print suggestionToBeViewed
		return render(request,self.template_name,{
			'form'			: formObj,

			})

class SuggestionList(ListView):

	template_name = 'suggestionlist.html'

	def get(self,request,*args,**kwargs):

		suggestionList = None
		if request.user.is_authenticated():

			suggestedBy = request.user
			suggestionList = SuggestedSongs.objects.filter(suggestedTo=suggestedBy.id,isSeen=False)

		return render(request,self.template_name,{
			'suggestions' 		: suggestionList
			})

	def post(self,request,*args,**kwargs):

		suggestionList = None
		points_key = {
			"cantsay"		: 5,
			"abitlike"		: 25,
			"superawesome"	: 50,
			"ok"		:	15,
			"bad"		:	-10,
			"what"		:	-50,
		}
		if request.user.is_authenticated():
			suggestedBy = request.user
			suggestionList = SuggestedSongs.objects.filter(suggestedTo=suggestedBy.id,isSeen=False)
			suggestionId = request.POST["suggestionId"]
			scoreString  = request.POST["scoreString"]

			points = points_key[scoreString]
			print suggestionId,scoreString,points

			suggestedSong = SuggestedSongs.objects.filter(id=suggestionId)[0]
			SuggestedSongs.objects.filter(id=suggestionId).update(isSeen=True,score=points)
			suggestedBy = suggestedSong.suggestedBy
			# suggestedSong.update(isSeen=True)
			# suggestedSong.update(score=points)
			print suggestedBy.id,suggestedBy.username
			msg = 'You have given %s points to %s' % (points,suggestedBy.username)
			print msg
			suggestionList = SuggestedSongs.objects.filter(suggestedTo=suggestedBy.id,isSeen=False)
			print '******',suggestionList

		return HttpResponseRedirect('/suggest')

class MyPlayList(ListView):
	template_name = 'myplaylist.html'

	def get(self,request,*args,**kwargs):
		songs = None

		if request.user.is_authenticated():

			songs = SuggestedSongs.objects.filter(suggestedTo=request.user).order_by('-score')


		return render(request,self.template_name,{
			'songs'		: songs
			})


class UpdateSongScoreAjax(ListView):

	def get(self,request,*args,**kwargs):

		d={}

		points_key = {
			"cantsay"		: 5,
			"abitlike"		: 25,
			"superawesome"	: 50,
			"ok"		:	15,
			"bad"		:	-10,
			"what"		:	-50,
		}

		suggestionId = self.kwargs["suggestionId"]
		scoreString  = self.kwargs["scoreString"]
		points = points_key[scoreString]
		print suggestionId,scoreString,points

		suggestedSong = SuggestedSongs.objects.filter(id=suggestionId)[0]
		suggestedBy = suggestedSong.suggestedBy
		print suggestedBy.id,suggestedBy.username
		msg = 'You have given %s points to %s' % (points,suggestedBy.username)
		print msg


		return HttpResponse(json.dumps(msg))


