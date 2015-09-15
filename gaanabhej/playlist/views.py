import urllib2
from lxml import etree

from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from .forms import PlayListForm
from playlist.models import SongDetails,SuggestedSongs


def convertToInt(no):
	no = no.replace(',','')
	return int(no)

class PlayList(ListView):

	template_name		= 'playlist.html'


	def get(self,request,*args,**kwargs):

		formObj			= PlayListForm(request.GET)
		suggestionToBeViewed = None 

		if formObj.is_valid():

			formCleaned 		= formObj.cleaned_data
			songURL				= formCleaned.get("songName",None)

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

				suggestedTo = User.objects.get(id=2)
				suggestedBy = request.user
				print suggestedBy,suggestedTo

				suggestion = SuggestedSongs(suggestedTo=suggestedTo,
					suggestedBy=suggestedBy,song=newsong,isSeen=False)
				suggestion.save()

				suggestionToBeViewed = SuggestedSongs.objects.filter(suggestedTo=suggestedBy,isSeen=False)
				print suggestionToBeViewed
		return render(request,self.template_name,{
			'form'			: formObj,
			'suggestions'	: suggestionToBeViewed

			})
