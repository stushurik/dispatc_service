from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from core.views import IndexView, LoginFormView, AuthenticationView, LogoutView, FileFormView, FileLoadView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from decisions.views import CreateDecisionView
from dispatch_service import settings

admin.autodiscover()
from events.views import CreateEventView, ListEventView, UpdateEventView, ListUserEventView, EventDetailView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dispatch_service.views.home', name='home'),
    # url(r'^dispatch_service/', include('dispatch_service.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^login/confirm/$', AuthenticationView.as_view(), name='confirm'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^accounts/', include('registration.urls')),

    url(r'^events$', ListEventView.as_view(), name='events-list'),
    url(r'^my-events$', ListUserEventView.as_view(), name='my-events-list'),
    url(r'^events/add$', CreateEventView.as_view(), name='events-new'),
    url(r'^events/edit/(?P<pk>\d+)/$', UpdateEventView.as_view(), name='events-edit'),
    url(r'^events/(?P<pk>\d+)/$', EventDetailView.as_view(), name='events-detail'),

    url(r'^events/(?P<pk>\d+)/resolve$', CreateDecisionView.as_view(), name='decisions-new'),

    url(r'^file-form$', FileFormView.as_view(), name='fileform'),
    url(r'^file$', FileLoadView.as_view(), name='file_load'),
)


urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
urlpatterns += staticfiles_urlpatterns()