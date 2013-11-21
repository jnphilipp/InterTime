import django.conf.urls


urlpatterns = django.conf.urls.patterns('django.contrib.auth.views',
    django.conf.urls.url(r'^login/$', 'login', {'template_name': 'userauth/login.html'},
        name='userauth_login'),
    django.conf.urls.url(r'^logout/$', 'logout', {'next_page': '/'},
        name='userauth_logout'),
    django.conf.urls.url(r'^password_change/$', 'password_change',
        {'template_name': 'userauth/password_change_form.html'},
        name='userauth_password_change'),
    django.conf.urls.url(r'^password_change_done/$', 'password_change_done',
        {'template_name': 'userauth/password_change_done.html'},
        name='userauth_password_change_done')
)


from django.views.generic import TemplateView

urlpatterns += django.conf.urls.patterns('',
    django.conf.urls.url(r'^register/$', 'userauth.views.register',
        {'next_page_name': 'userauth_register_done'},
        name='userauth_register'),
    django.conf.urls.url(r'^welcome/$',
        TemplateView.as_view(template_name='userauth/register_done.html'),
        name='userauth_register_done'),
    django.conf.urls.url(r'^plan/$', TemplateView.as_view(template_name='userauth/plan.html'),name= 'user_plan')
)
