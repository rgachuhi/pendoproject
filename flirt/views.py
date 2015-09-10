
from .serializers import (PreferencesSerializer, 
                          MatchSerializer, ChatMessageSerializer, ChatStreamSerializer)
from .models import (Match, Preferences, ChatMessage, ChatStream)
from rest_framework.renderers import JSONRenderer
from users.serializers import (UserSerializer)

from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseServerError
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
from django.contrib.gis.geos.factory import fromstr
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.shortcuts import get_object_or_404
from datetime import *
from dateutil.relativedelta import relativedelta
from django.db.models import Q

import redis

User = get_user_model()

# Get an instance of a logger
logger = logging.getLogger(__name__)

class RegisterViewSet(viewsets.ViewSet):
    def list_matches(self, request):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            User.objects.create_user(
            serialized.init_data['email'],
            serialized.init_data['date_of_birth'],
            serialized.init_data['password']
        )
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
        

class NearestUserViewSet(viewsets.GenericViewSet): 
    serializer_class = UserSerializer
    #permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    
    def get_nearest(self, request, *args, **kwargs):
        #-82.1013183593750000 40.1766586303710014
        logger.error('NearestUserViewSet: ' +kwargs['latitude']+' '+kwargs['longitude'])
        current_user = request.user
        
        pref_qs = Preferences.objects.all()
        preferences = get_object_or_404(pref_qs, user=current_user)
        # Get the current date
        now = date.today()
        
        min_date = now - relativedelta(years=preferences.max_age)
        max_date = now - relativedelta(years=preferences.min_age)
        
        logger.error('min_date ' + str(min_date))
        logger.error('max_date ' + str(max_date))
        
        distance_pref = preferences.distance
        gender_pref = preferences.gender_pref
        logger.error('Preferences: Gender ' + gender_pref + ' distance ' + str(distance_pref))
        # Filter for all prospects already processed by user
        match_set = Match.objects.filter(Q(source=current_user) | Q(target=current_user)).all()
        #for prospect in match_set:
        email_set = set()
        for x in match_set:
            logger.error('Matched emails ' + x.source.email +' and ' + x.target.email)
            email_set.add(x.source.email)
            email_set.add(x.target.email)
        
        #email_set = {y.email for x in match_set for y in x.users.all()}   #set()
        
        # Exclude login user
        '''email_set.add(current_user.email)
        for match in match_set:
            email_set.add(match.)'''
        
        gps_reading = fromstr('POINT('+kwargs['latitude']+' '+kwargs['longitude']+')', srid=4326)
        nearest_users = User.geo.exclude(email__in=email_set).exclude(preferences__hidden=True).filter(Q(date_of_birth__gte=min_date) & Q(date_of_birth__lte=max_date))
        nearest_users = nearest_users.filter(gender=gender_pref).filter(location__distance_lte=(gps_reading, D(mi=distance_pref))).distance(gps_reading).order_by('distance')
    
        paginator = PageNumberPagination()
       
        result_page = paginator.paginate_queryset(nearest_users.all(), request)
        
        serializer = UserSerializer(result_page , many=True)
        return paginator.get_paginated_response(serializer.data)
 
class MatchesViewSet(viewsets.ViewSet):
    #permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    
    def list_matches(self, request):
        current_user = request.user
        match_set = Match.objects.filter(Q(target=current_user) | (Q(source=current_user)) & Q(status='matched')).exclude(
                                                Q(status='rejected') | Q(status='chat')).all()
        #Q(status='liked') | 
        
        serializer = MatchSerializer(match_set, context={'user_email': current_user.email}, many=True)
        return Response(serializer.data)
    
    def match_make(self, request):
        current_user = request.user
        data = request.data;
        email = data['email']
        logger.error('match_make email ' + email)
        queryset = User.objects.all()
        other_user = get_object_or_404(queryset, email=email)
        
        #:TODO: if a prospect is found, update status to matched or rejected
        match = None
        try:
            match = Match.objects.get(Q(source=current_user) | Q(target=current_user), Q(source=other_user) | Q(target=other_user))
                    
            if match is None:
                raise Exception('No Match found')
            
            if data['status'] == 'rejected':
                match.status = 'rejected'
                
            if data['status'] == 'liked':
                if match.status == 'rejected':
                    match.save()
                    return Response({'status': 'rejected'})
                elif match.status == 'liked':
                    match.status = 'matched'
                    match.save()
            
            match.date_updated=datetime.now()
            match.save()
        except Exception:
            logger.error('Creating new match')
            match = Match.objects.create(source=current_user, target=other_user)
            if data['status'] == 'rejected':
                match.status = 'rejected'
            match.save()
            
        serializer = MatchSerializer(match)
        return Response(serializer.data)
        
        
class PreferencesViewSet(viewsets.ViewSet):
    #permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    
    def retrieve_prefs(self, request):
        current_user = request.user
        queryset = Preferences.objects.all()
        preferences = get_object_or_404(queryset, user=current_user)
        serializer = PreferencesSerializer(preferences)
        return Response(serializer.data)
    
    def update_prefs(self, request):
        current_user = request.user
        queryset = Preferences.objects.all()
        preferences = get_object_or_404(queryset, user=current_user)
        serializer = PreferencesSerializer(preferences, data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save(date_updated=datetime.now())
            return Response({'status': 'preferences updated'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
class ChatStreamViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    
    def streams_all(self, request):
        current_user = request.user
        queryset = ChatStream.objects.filter(Q(user1=current_user) | Q(user2=current_user)).all()
        serializer = ChatStreamSerializer(queryset, context={'user_email': current_user.email}, many=True)
        return Response(serializer.data)
    
    def chats_list(self, request, *args, **kwargs):
        stream_id = kwargs['stream_id'] 
        logger.error('StreamId ' + stream_id)
        queryset = ChatStream.objects.all()
        chat_stream = get_object_or_404(queryset, id=stream_id)
        chat_messages = chat_stream.chatmessage_set.all()
        logger.error('To Serializer ')
        serializer = ChatMessageSerializer(chat_messages, many=True)
        return Response(serializer.data)
    
    def stream_create(self, request):
        current_user = request.user
        email = request.data['email']
        match_id = request.data['match_id']
        queryset = User.objects.all()
        other_user = get_object_or_404(queryset, email=email)
        
        chat_stream = None
        try:
            chat_stream = ChatStream.objects.get(Q(user1=current_user) | Q(user2=current_user), Q(user1=other_user) | Q(user2=other_user))
            if chat_stream is None:
                raise Exception('No ChatStream found')
        except Exception:
            match = Match.objects.get(id=match_id)
            match.status = 'chat'
            match.date_updated=datetime.now()
            match.save()
            chat_stream = ChatStream.objects.create(user1 = current_user, user2 = other_user)
            logger.error('ChatStream new created ' + str(chat_stream.id))
        serializer = ChatStreamSerializer(chat_stream, context={'user_email': current_user.email})
        return Response(serializer.data)
        
class ChatViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    
    def chat_create(self, request):
        try:
            current_user = request.user
            stream_id = request.data.get('stream')
            target_email = request.data.get('target')
            queryset = User.objects.all()
            target_user = get_object_or_404(queryset, email=target_email)
            message_data = request.data.get('message')
            queryset = ChatStream.objects.all()
            chat_stream = get_object_or_404(queryset, id=stream_id)
            logger.error('chat create 1')
            # Create chat message
            chat_message = ChatMessage.objects.create(stream=chat_stream, sender=current_user, receiver=target_user, message=message_data)
            
            serializer = ChatMessageSerializer(chat_message)
            json = JSONRenderer().render(serializer.data)
            # Once chat has been created post it to the chat channel
            r = redis.StrictRedis(host='localhost', port=6379, db=0)
            r.publish('chat', json)
            logger.error('ChatMessage created ' + str(json))
            return Response({'status': 'Chat message saved'})
        except Exception as e:
            return HttpResponseServerError(str(e))

