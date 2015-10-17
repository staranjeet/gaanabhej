from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static        import static
from django.conf	import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib                 import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import  RedirectView
from django.contrib.auth            import views as auth_views

from playlist.views import ( 
                SuggestASong,SuggestionList,
                MyPlayList,MyOwnSuggestion,
                AddSongToPlayList
                )


urlpatterns = [
    # Examples:
    # url(r'^$', 'gaanabhej.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^accounts/login/$',auth_views.login,{'template_name' : 'django-auth/login.html'}),
    url('^logout/$', auth_views.logout, {'template_name' : 'registration/logged_out.html'}),
    url('^', include('django.contrib.auth.urls')),
    url(r'^suggest', SuggestASong.as_view(), name='suggest_song'),
    # url(r'^$', RedirectView.as_view(url=reverse_lazy('suggest_song')), name='play-list'),
    url(r'^myplaylist$', MyPlayList.as_view(), name='my_play_list'),
    url(r'^mysuggestions$', MyOwnSuggestion.as_view(), name='my_suggestions'),
    url(r'^songs', SuggestionList.as_view(), name='suggestion_list'),
    url(r'^addsong', AddSongToPlayList.as_view(), name='add-to-playlist'),
    url(r'^songs/(?P<suggestionId>[0-9]+)/(?P<scoreString>[-\w]+)/', SuggestionList.as_view(), name='suggestion_list'),

    # url(r'^ajax/score/(?P<suggestionId>[0-9]+)/(?P<scoreString>[-\w]+)/$',UpdateSongScoreAjax.as_view(),name="update-score-ajax-view"),

    # url(r'^accounts/logout/$',auth_views.logout),



    url(r'^admin/', include(admin.site.urls)),
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
