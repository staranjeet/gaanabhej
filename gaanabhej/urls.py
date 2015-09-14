from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static        import static
from django.conf	import settings

from playlist.views import PlayList

urlpatterns = [
    # Examples:
    # url(r'^$', 'gaanabhej.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', PlayList.as_view(), name='play-list'),

    url(r'^admin/', include(admin.site.urls)),
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
