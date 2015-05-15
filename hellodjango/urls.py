from django.conf.urls import patterns, include, url
from django.contrib import admin
from hellodjango import views
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hellodjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
	url(r'^static/(?P.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})
	#url(r'^$', 'hellodjango.myapp.views.home', name='home'),
	
)
