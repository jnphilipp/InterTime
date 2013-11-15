from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'timetable.views.index'),
	url(r'^timetable/$', 'timetable.views.index'),
	url(r'^timetable/(?P<modul_id>\d+)/$', 'timetable.views.details', name='blog-post'),
	url(r'^admin/', include(admin.site.urls)),
)