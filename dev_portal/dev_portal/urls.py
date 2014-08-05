from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'links.views.index', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^links/', include('links.urls', namespace='links')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^wanikani/', include('wanikani.urls', namespace='wanikani')),
)
