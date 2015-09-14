from django.shortcuts import render
from django.views.generic import ListView

from .forms import PlayListForm

class PlayList(ListView):

	template_name		= 'playlist.html'


	def get(self,request,*args,**kwargs):

		formObj			= PlayListForm(request.GET)

		if formObj.is_valid():

			formCleaned 		= formObj.cleaned_data
			songName			= formCleaned.get("songName",None)

			if songName is not None:
				pass

		return render(request,self.template_name,{
			'form'			: formObj

			})
