from django.conf.urls import patterns, include, url

from core.views import IndexView, LoginFormView, AuthenticationView, LogoutView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from events.views import CreateEventView, ListEventView, UpdateEventView

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

    url(r'^events$', ListEventView.as_view(), name='events-list'),
    url(r'^events/add$', CreateEventView.as_view(), name='events-new'),
    url(r'^events/edit/(?P<pk>\d+)/$', UpdateEventView.as_view(), name='events-edit'),
)
