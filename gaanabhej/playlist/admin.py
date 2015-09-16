from django.contrib import admin
from .models import SongDetails,SuggestedSongs

class SongDetailsAdmin(admin.ModelAdmin):

	list_per_page 				= 100
	list_display				= ('name','url','views','likes','dislikes')
	list_display_links			= ['name',]
	search_fields 				= ['name',]


class SuggestedSongsAdmin(admin.ModelAdmin):

	list_per_page 				= 100
	list_display 				= ('id','song','suggestedBy','suggestedTo','isSeen','score')
	list_display_links 			= ['id','song',]
	search_fields 				= ['song']
	list_filter 				= ['song','suggestedBy','suggestedTo','isSeen']

	
admin.site.register(SongDetails,SongDetailsAdmin)
admin.site.register(SuggestedSongs,SuggestedSongsAdmin)