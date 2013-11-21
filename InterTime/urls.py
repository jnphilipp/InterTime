from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'timetable.views.index'),
	url(r'^user/', include('userauth.urls')),
	url(r'^timetable/$', 'timetable.views.moduls'),
	url(r'^timetable/(?P<modul_id>\d+)/$', 'timetable.views.details', name='blog-post'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^departments/$', 'timetable.views.departments'),
	url(r'^department/(?P<department_id>\d+)/$', 'timetable.views.department_details', name='blog-post'),
	url(r'^plan/$', 'timetable.views.plan' ,name= 'Semesterplan'),
)
