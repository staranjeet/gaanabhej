from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static        import static
from django.conf	import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib                 import admin
from django.contrib.auth            import views as auth_views

from playlist.views import SuggestASong,UpdateSongScoreAjax,SuggestionList,MyPlayList

urlpatterns = [
    # Examples:
    # url(r'^$', 'gaanabhej.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', SuggestASong.as_view(), name='play-list'),
    url(r'^suggest$', SuggestASong.as_view(), name='play-list'),
    url(r'^myplaylist$', MyPlayList.as_view(), name='play-list'),
    url(r'^songs', csrf_exempt(SuggestionList.as_view()), name='play-list'),
    url(r'^songs/(?P<suggestionId>[0-9]+)/(?P<scoreString>[-\w]+)/', csrf_exempt(SuggestionList.as_view()), name='play-list'),

    url(r'^ajax/score/(?P<suggestionId>[0-9]+)/(?P<scoreString>[-\w]+)/$',UpdateSongScoreAjax.as_view(),name="update-score-ajax-view"),

    url(r'^accounts/login/$',auth_views.login),
    url(r'^accounts/logout/$',auth_views.logout),



    url(r'^admin/', include(admin.site.urls)),
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
