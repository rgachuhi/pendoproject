'''
Created on Apr 8, 2015

@author: Raphael
'''
from django.conf.urls import patterns, include, url
from rest_framework import routers
from .views import PreferencesViewSet, ChatStreamViewSet, MatchesViewSet, NearestUserViewSet, ChatViewSet

pref_details = PreferencesViewSet.as_view({
    'get': 'retrieve_prefs'
})

pref_update = PreferencesViewSet.as_view({
    'post': 'update_prefs'
})

list_chats = ChatStreamViewSet.as_view({
    'get': 'chats_list'
})

all_streams = ChatStreamViewSet.as_view({
    'get': 'streams_all'
})

stream_create = ChatStreamViewSet.as_view({
    'post': 'stream_create'
})

chat_create = ChatViewSet.as_view({
    'post': 'chat_create'
})

match_list = MatchesViewSet.as_view({
    'get': 'list_matches'
})

match_make = MatchesViewSet.as_view({
    'post': 'match_make'
})

nearest_list = NearestUserViewSet.as_view({
    'get': 'get_nearest'
})

# Routers provide an easy way of automatically determining the URL conf.
'''router = routers.DefaultRouter(trailing_slash=False)

router.register(r'prospects', ProspectViewSet, 'matches')
router.register(r'prefs', PreferencesViewSet, 'prefs')
router.register(r'chatstream', ChatStreamViewSet, 'chats')
router.register(r'nearest/(?P<latitude>.+)/(?P<longitude>.+)', NearestUserViewSet, 'nearest-list')

urlpatterns = router.urls'''

urlpatterns = patterns('',
    url(r'^nearest/(?P<latitude>.+)/(?P<longitude>.+)/list', nearest_list, name='nearest-list'),
    url(r'^matches/make', match_make, name='match-make'),
    url(r'^matches/list', match_list, name='match-list'),
    url(r'^chats/streams_all', all_streams, name='streams-all'),
    url(r'^chats/list/(?P<stream_id>.+)', list_chats, name='chats-list'),
    url(r'^chats/stream_create', stream_create, name='stream-create'),
    url(r'^chat/chat_create', chat_create, name='chat-create'),
    url(r'^prefs/get', pref_details, name='pref-details'),
    url(r'^prefs/update', pref_update, name='pref-update')
)