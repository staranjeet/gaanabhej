from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
					SongDetails,
					SuggestedSongs,
					UserProfile)

@admin.register(SongDetails)
class SongDetailsAdmin(admin.ModelAdmin):

	list_per_page 				= 100
	list_display				= ('name','url','views','likes','dislikes')
	list_display_links			= ['name',]
	search_fields 				= ['name',]


@admin.register(SuggestedSongs)
class SuggestedSongsAdmin(admin.ModelAdmin):

	list_per_page 				= 100
	list_display 				= ('id','song','suggestedBy','suggestedTo','isSeen','score')
	list_display_links 			= ['id','song',]
	search_fields 				= ['song']
	list_filter 				= ['song','suggestedBy','suggestedTo','isSeen']

	
class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'User'


class UserAdmin(UserAdmin):
	inlines = (UserProfileInline, )
	list_display = ('username', 'email', 'first_name', 'display_score')

	def display_score(self, request):
		if UserProfile.objects.filter(user__id=request.id):
			return UserProfile.objects.get(user__id=request.id).score
		else:
			return None
		display_name.short_description = 'Score'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# admin.site.register(SongDetails,SongDetailsAdmin)
# admin.site.register(SuggestedSongs,SuggestedSongsAdmin)