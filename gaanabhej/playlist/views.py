import requests,json
from lxml import etree

from django.shortcuts 					import render
from django.contrib.auth.models 		import User
from django.db.models 					import Q
from django.http 						import HttpResponse,HttpResponseRedirect
from django.template.context_processors import csrf
from django.utils.safestring 			import mark_safe
from django.core.context_processors 	import csrf
from django.template 					import RequestContext
from django.views.generic.detail 		import SingleObjectMixin
from django.utils.decorators            import method_decorator
from django.contrib.auth.decorators     import login_required
from django.views import generic
from django.core.mail import send_mail

from playlist.models import (
							SongDetails,
							SuggestedSongs,
							MySongModel,
							UserProfile)
from playlist.forms import (
						AddSongToPlayListForm,
						SuggestSongForm)


def convertToInt(no):
	'''
	To convert numbers like 424,456 into 424567
	'''
	no = no.replace(',','')
	return int(no)

def return_song_details(url):

	try:
		page			= requests.get(url).text
		x	 			= etree.HTML(page)
		title			= x.xpath('//title/text()')[0]
		views			= convertToInt(x.xpath('//div[@class="watch-view-count"]/text()')[0])
		likes			= convertToInt(x.xpath('//button[@title="Unlike"]/span[@class="yt-uix-button-content"]/text()')[0])
		dislikes		= convertToInt(x.xpath('//button[@title="I dislike this"]/span[@class="yt-uix-button-content"]/text()')[0])
	except Exception as e:
		print 'Error : Parsing song info ',e
		title,views,likes,dislikes = [None]*4
	
	return (title, views, likes, dislikes)

def custom_send_mail(recipient, sender, subject, message):

	send_mail(subject, message, sender, recipient, fail_silently=True)

class SuggestASong(generic.CreateView):

	template_name = 'newSuggestion.html'
	# form_class = SuggestSongForm

	# def get_form_kwargs(self, **kwargs):
	# 	form_kwargs = super(SuggestASong, self).get_form_kwargs(**kwargs)
	# 	form_kwargs['user'] = self.request.user
	# 	return form_kwargs

	# def get_queryset(self):
	# 	return Suggest

	def get(self,request,*args,**kwargs):

		formObj			= SuggestSongForm(request.GET,user=request.user)
		return render(request,self.template_name,{
			'form'			: formObj,
			})

	def post(self,request,*args,**kwargs):

		parseError 				= False
		alertMsg, alrtBstrpCls 	= [None]*2
		d 						= {}

		if request.user.is_authenticated():
			suggestedBy			= request.user
			songURL				= request.POST.get("songName",None)
			suggestedToId 		= request.POST.get("suggestedTo",None)
			suggestedTo 		= User.objects.get(id=suggestedToId)
			# print suggestedBy.id ,'suggesting to ', suggestedToId

			if songURL is not None:

				# before parinsg info for song, check if this song is already
				# suggested or not
				isSongPresent 		= SuggestedSongs.objects.filter(suggestedTo=suggestedToId,
										suggestedBy=suggestedBy.id,song__url=songURL)
				if isSongPresent:
					# means that the song is already suggested
					alertMsg 	= '''Oops!! Looks like you have already suggested  
									this song to {user}'''.format(user=suggestedTo.username)
					alrtBstrpCls = 'alert-info'

				else:

					title, views, likes, dislikes = return_song_details(songURL)

					if title is not None:
						newsong = SongDetails(
							url=songURL,name=title,views=views,
							dislikes=dislikes,likes=likes
							)
						newsong.save()
						suggestion = SuggestedSongs(suggestedTo=suggestedTo,
							suggestedBy=suggestedBy,song=newsong,isSeen=False)
						suggestion.save()
						# notify 
						senderEmail = suggestedBy.email
						senderName = suggestedBy.username
						recipientEmail = [suggestedTo.email]
						subject = '{0} has suggested you a song'.format(senderName)
						message = '{0} has suggested you {1}'.format(senderName, title)
						# dont delete this comment
						# custom_send_mail(recipientEmail, senderEmail, subject, message)

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

		d = {
			'alrtBstrpCls'	: alrtBstrpCls,
			'alertMsg'		: alertMsg
		}
		return HttpResponse(json.dumps(d))


class SuggestionList(generic.ListView):

	template_name = 'suggestionList.html'

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
			"ok"			: 15,
			"bad"			: -10,
			"what"			: -50,
		}

		if request.user.is_authenticated():
			suggestedTo = request.user
			suggestionList = SuggestedSongs.objects.filter(suggestedTo=suggestedTo.id,isSeen=False)
			suggestionId = request.POST["suggestionId"]
			scoreString  = request.POST["scoreString"]

			points = points_key[scoreString]
			# print suggestionId,scoreString,points

			suggestedSong = SuggestedSongs.objects.filter(id=suggestionId)[0]
			SuggestedSongs.objects.filter(id=suggestionId).update(isSeen=True,score=points)
			suggestedBy = suggestedSong.suggestedBy
			existingProfile = UserProfile.objects.get(user__id=suggestedBy.id)
			existingProfile.score += points
			# print 'updated points', existingProfile.score 
			existingProfile.save()
			# UserProfile.objects.get(user__id=suggestedBy.id).update(updatedPoints)
			msg = 'You have given %s points to %s' % (points,suggestedBy.username)
			# print msg,suggestedTo.id
			suggestionList = SuggestedSongs.objects.filter(suggestedTo=suggestedTo.id,isSeen=False)

		return render(request,'suggestAjax.html',{
			'suggestions' 		: suggestionList
			})


class MyPlayList(SingleObjectMixin, generic.ListView):
	context_object_name = 'songs'
	template_name = 'playlist.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(MyPlayList,self).dispatch(*args, **kwargs)
	def get_queryset(self):
		return SuggestedSongs.objects.filter(suggestedTo=self.request.user).order_by('-score')

	# def get(self,request,*args,**kwargs):
	# 	songs = None

	# 	if request.user.is_authenticated():

	# 		songs = SuggestedSongs.objects.filter(suggestedTo=request.user).order_by('-score')

	# 	return render(request,self.template_name,{
	# 		'songs'		: songs
	# 		})

class MyOwnSuggestion(generic.ListView):
	template_name = 'myOwnSuggestion.html'
	context_object_name = 'ownSuggestions'

	def get_queryset(self):
		return SuggestedSongs.objects.filter(suggestedBy=self.request.user.id)

	def get_context_data(self,**kwargs):
		context = super(MyOwnSuggestion, self).get_context_data(**kwargs)
		msg = '''Oops! Looks like you not have not suggested any song. No issues.
					Suggesting a song is very easy. Just paste in the youtube url and 
					select the user and Voila. Your song is suggested to him
				'''
		ownSuggestions = len(self.get_queryset())
		if ownSuggestions > 0:
			msg = ''' Uptill now you have suggested %s songs
			   ''' % (ownSuggestions)
		context['msg'] = msg
		return context

class AddSongToPlayList(generic.CreateView):

	template_name = 'addSongToPlaylist.html'
	form_class = AddSongToPlayListForm

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(AddSongToPlayList,self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):

		d = {}
		alertMsg = '''We are facing some error in retriving  
					media info. Can you please try again later'''
		bstrpCls = 'alert-danger'
		if request.user.is_authenticated():
			songURL = request.POST.get('url', None)
			if songURL:
				title, views, likes, dislikes = return_song_details(songURL)
				if title:
					try:
						newsong = SongDetails.objects.get(url=songURL)
					except:
						newsong = SongDetails(
							url=songURL, name=title, views=views,
							dislikes=dislikes, likes=likes)
						newsong.save()
					mySongInPlaylist, created =  MySongModel.objects.get_or_create(
										song=newsong, owner=request.user)
					if not created:
						alertMsg = 'Looks like this song is already in your playlist'
						bstrpCls = 'alert-warning'
					else:
						alertMsg = mark_safe('''%s is now added in your playlist.''' % (
										title))
						bstrpCls = 'alert-info'
		d['alertMsg'] = alertMsg
		d['alrtBstrpCls'] = bstrpCls
		return HttpResponse(json.dumps(d))

