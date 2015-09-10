from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
#from django.contrib.gis import admin as gisadmin
from django.views.generic import RedirectView
from flirtupendo import views


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/docs')),
    
    url(r'^', include('flirt.urls')),
    url(r'^', include('users.urls')),
    
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^api-token-auth', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    
    url(r'^docs/', include('rest_framework_swagger.urls')),
    
    url(r'^status/$', views.StatusView.as_view(), name='status'),
    url(r'^authenticated/$', views.AuthenticationTestView.as_view(), name='authenticated'),
    url(r'^health/$', views.HealthView.as_view(), name='health'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)

if settings.ENABLE_ADMIN_SITE:  # pragma: no cover
    admin.autodiscover()
    #gisadmin.autodiscover()
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls)),
       # url(r'^gis/', include(gisadmin.site.urls)),
    )

handler500 = 'flirtupendo.views.handle_internal_server_error'  # pylint: disable=invalid-name
handler404 = 'flirtupendo.views.handle_missing_resource_error'  # pylint: disable=invalid-name