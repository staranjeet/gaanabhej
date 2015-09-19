import requests,json
from lxml import etree

from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from django.template.context_processors import csrf
from django.utils.safestring import mark_safe

from .forms import PlayListForm
from playlist.models import SongDetails,SuggestedSongs


def convertToInt(no):
	no = no.replace(',','')
	return int(no)

class SuggestASong(ListView):

	template_name		= 'newSuggestion.html'


	def get(self,request,*args,**kwargs):

		formObj			= PlayListForm(request.GET,user=request.user)
		# suggestionToBeViewed = None
		# parseError = False
		# alertMsg, alrtBstrpCls = [None]*2
		
		# suggestedBy = request.user

		# if formObj.is_valid():

		# 	formCleaned 		= formObj.cleaned_data
		# 	songURL				= formCleaned.get("songName",None)
		# 	suggestedToId 		= formCleaned.get("suggestedTo",None)
		# 	suggestedTo 		= User.objects.get(id=suggestedToId)
		# 	# print suggestedBy,suggestedTo

		# 	if songURL is not None:
		# 		print songURL
		# 		try:
		# 			page			= requests.get(songURL).text
		# 			x	 			= etree.HTML(page)
		# 			title			= x.xpath('//title/text()')[0]
		# 			views			= convertToInt(x.xpath('//div[@class="watch-view-count"]/text()')[0])
		# 			likes			= convertToInt(x.xpath('//button[@title="Unlike"]/span[@class="yt-uix-button-content"]/text()')[0])
		# 			dislikes		= convertToInt(x.xpath('//button[@title="I dislike this"]/span[@class="yt-uix-button-content"]/text()')[0])
		# 		except Exception,e:
		# 			print 'Error : Parsing song info ',e
		# 			title,views,likes,dislikes = [None]*4
		# 			parseError = True
		# 		# duration 		= x.xpath('//span[@class="video-time"]/text()')
		# 		# print title,views,likes,dislikes
		# 		if not parseError:
		# 			newsong = SongDetails(
		# 				url=songURL,name=title,views=views,
		# 				dislikes=dislikes,likes=likes
		# 				)
		# 			newsong.save()
		# 			suggestion = SuggestedSongs(suggestedTo=suggestedTo,
		# 				suggestedBy=suggestedBy,song=newsong,isSeen=False)
		# 			suggestion.save()

		# 			alertMsg 	= mark_safe('''Your song is successfully suggested to %s. 
		# 						By the ways it was a %s song''' % (
		# 							suggestedTo.username,
		# 							'<i class="glyphicon glyphicon-heart"></i>'
		# 							))
		# 			alrtBstrpCls = 'info'



		# 		else:
		# 			alertMsg	 = '''We are facing some error in retriving  
		# 							media info. Can you please try again later'''
		# 			alrtBstrpCls  = 'danger'

		# suggestionToBeViewed = SuggestedSongs.objects.filter(suggestedTo=suggestedBy.id,isSeen=False)
		# print suggestionToBeViewed
		return render(request,self.template_name,{
			'form'			: formObj,
			# 'alrtBstrpCls'	: alrtBstrpCls,
			# 'alertMsg'		: alertMsg

			})

	def post(self,request,*args,**kwargs):

		# formObj					= PlayListForm(request.GET,user=request.user)
		suggestionToBeViewed 	= None
		parseError 				= False
		alertMsg, alrtBstrpCls 	= [None]*2
		d 						= {}
		

		if request.user.is_authenticated():
			suggestedBy			= request.user
			songURL				= request.POST.get("songName",None)
			suggestedToId 		= request.POST.get("suggestedTo",None)
			suggestedTo 		= User.objects.get(id=suggestedToId)

			if songURL is not None:
				# print songURL
				try:
					page			= requests.get(songURL).text
					x	 			= etree.HTML(page)
					title			= x.xpath('//title/text()')[0]
					views			= convertToInt(x.xpath('//div[@class="watch-view-count"]/text()')[0])
					likes			= convertToInt(x.xpath('//button[@title="Unlike"]/span[@class="yt-uix-button-content"]/text()')[0])
					dislikes		= convertToInt(x.xpath('//button[@title="I dislike this"]/span[@class="yt-uix-button-content"]/text()')[0])
				except Exception,e:
					print 'Error : Parsing song info ',e
					title,views,likes,dislikes = [None]*4
					parseError = True
				# duration 		= x.xpath('//span[@class="video-time"]/text()')
				# print title,views,likes,dislikes
				if not parseError:
					newsong = SongDetails(
						url=songURL,name=title,views=views,
						dislikes=dislikes,likes=likes
						)
					newsong.save()
					suggestion = SuggestedSongs(suggestedTo=suggestedTo,
						suggestedBy=suggestedBy,song=newsong,isSeen=False)
					suggestion.save()

					alertMsg 	= mark_safe('''Your song is successfully suggested to %s. 
								What a %s suggestion''' % (
									suggestedTo.username,
									'<i class="glyphicon glyphicon-heart"></i>'
									))
					alrtBstrpCls = 'alert-info'
				else:
					alertMsg	 = '''We are facing some error in retriving  
									media info. Can you please try again later'''
					alrtBstrpCls  = 'alert-danger'

		# return render(request,self.template_name,{
		# 	'form'			: formObj,
		# 	'alrtBstrpCls'	: alrtBstrpCls,
		# 	'alertMsg'		: alertMsg

		# 	})
		d = {
			'alrtBstrpCls'	: alrtBstrpCls,
			'alertMsg'		: alertMsg
		}
		return HttpResponse(json.dumps(d))



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
		# c = {}
		# c.update(csrf(request))
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
			# print suggestedBy.id,suggestedBy.username
			msg = 'You have given %s points to %s' % (points,suggestedBy.username)
			# print msg
			suggestionList = SuggestedSongs.objects.filter(suggestedTo=suggestedBy.id,isSeen=False)

		return render(request,'suggestAjax.html',{
			'suggestions' 		: suggestionList
			})

		# return HttpResponseRedirect('/suggest')

class MyPlayList(ListView):
	template_name = 'myplaylist.html'

	def get(self,request,*args,**kwargs):
		songs = None

		if request.user.is_authenticated():

			songs = SuggestedSongs.objects.filter(suggestedTo=request.user).order_by('-score')


		return render(request,self.template_name,{
			'songs'		: songs
			})


# class UpdateSongScoreAjax(ListView):

# 	def get(self,request,*args,**kwargs):

# 		d={}

# 		points_key = {
# 			"cantsay"		: 5,
# 			"abitlike"		: 25,
# 			"superawesome"	: 50,
# 			"ok"		:	15,
# 			"bad"		:	-10,
# 			"what"		:	-50,
# 		}

# 		suggestionId = self.kwargs["suggestionId"]
# 		scoreString  = self.kwargs["scoreString"]
# 		points = points_key[scoreString]
# 		print suggestionId,scoreString,points

# 		suggestedSong = SuggestedSongs.objects.filter(id=suggestionId)[0]
# 		suggestedBy = suggestedSong.suggestedBy
# 		print suggestedBy.id,suggestedBy.username
# 		msg = 'You have given %s points to %s' % (points,suggestedBy.username)
# 		print msg


# 		return HttpResponse(json.dumps(msg))


