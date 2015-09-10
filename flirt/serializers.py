'''
Created on Apr 8, 2015

@author: Raphael
'''
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from flirt.models import Preferences, ChatMessage, Match, ChatStream
from users.serializers import UserSerializer, UserImageSerializer
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Serializers define the API representation.
        
class MatchSerializer(serializers.ModelSerializer):
    source = UserSerializer()
    target = UserSerializer()
    created = serializers.DateTimeField(format=None, read_only=True)
    date_updated = serializers.DateTimeField(format=settings.DATETIME_FORMAT, read_only=True)
    tag = serializers.SerializerMethodField()
    class Meta:
        model = Match
        fields = ('id', 'source', 'target', 'status', 'tag', 'date_updated', 'created')
        
    def get_tag(self, obj):
        return self.context.get('user_email') == obj.source.email
    
    def create(self, validated_data):
        return Match.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.date_updated = validated_data.get('date_updated', instance.date_updated)
        instance.save()
        return instance

class PreferencesSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Preferences
        fields = ('user', 'min_age', 'max_age', 'gender_pref', 'distance', 'hidden')
    
    def get_email(self, obj):
        return obj.email
        
    def create(self, validated_data):
        return Preferences.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.min_age = validated_data.get('min_age', instance.min_age)
        instance.max_age = validated_data.get('max_age', instance.max_age)
        instance.gender_pref = validated_data.get('gender_pref', instance.gender_pref)
        instance.distance = validated_data.get('distance', instance.distance)
        instance.date_updated = validated_data.get('date_updated', instance.date_updated)
        instance.save()
        return instance

class ChatStreamIdSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = ChatStream
        fields = ('id',)
        
class ChatStreamSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    last = serializers.SerializerMethodField()
    user1 = UserSerializer()
    user2 = UserSerializer()
    tag1 = serializers.SerializerMethodField()
    class Meta:
        model = ChatStream
        fields = ('id', 'last', 'user1', 'user2', 'tag1')
    
    def get_last(self, obj):
        return 'No message yet'
        '''chat_messages = obj.chatmessage_set.order_by('created')
        if len(chat_messages.all()) == 0:
            return 'No message yet'
        return chat_messages.all()[0].message'''
    
    def get_tag1(self, obj):
        return self.context.get('user_email') == obj.user1.email
    
class ChatMessageSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format=settings.DATETIME_FORMAT, read_only=True)
    stream = ChatStreamIdSerializer()
    sender = UserImageSerializer()
    receiver = UserImageSerializer()
    class Meta:
        model = ChatMessage
        fields = ('stream', 'id', 'sender', 'receiver', 'message','created')
        
