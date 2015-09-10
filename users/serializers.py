
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.utils.timezone import now
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail
from dateutil.relativedelta import *
from datetime import *

User = get_user_model()

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'type': 'password'},
        required=False
    )

class UserImageSerializer(serializers.ModelSerializer):
    tiny_image = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('first_name','tiny_image',)
    
    def get_tiny_image(self, obj):
        image = get_thumbnail(obj.profile_image, '80x80', crop='top', quality=99)
        return settings.SITE_URL+image.url

class UserSerializer(serializers.ModelSerializer):
    #first_name = serializers.CharField(required=False)
    #last_name = serializers.CharField(required=False)
    email = serializers.EmailField()
    date_joined = serializers.DateTimeField(read_only=True)
    #date_of_birth = serializers.DateField(required=False)
    profile_image = serializers.SerializerMethodField() #serializers.ImageField(required=False)
    thumbnail = serializers.SerializerMethodField()
    tiny_image = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('email', 'first_name','gender', 'date_joined', 'age', 'profile_image', 'thumbnail', 'tiny_image', 'location',)
        
    def get_age(self, obj):
        # Get the current date
        now = date.today()
        #now = now.date()
    
        # Get the difference between the current date and the birthday
        age = relativedelta(now, obj.date_of_birth)
        age = age.years
    
        return age
    
    def get_profile_image(self, obj):
        return settings.SITE_URL+obj.profile_image.url
    
    def get_thumbnail(self, obj):
        image = get_thumbnail(obj.profile_image, '300x300', crop='top', quality=99)
        return settings.SITE_URL+image.url
    
    def get_tiny_image(self, obj):
        image = get_thumbnail(obj.profile_image, '80x80', crop='top', quality=99)
        return settings.SITE_URL+image.url

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True,
        required=False,
        slug_field='codename',
        queryset=Permission.objects.all()
    )

    class Meta:
        model = Group
        fields = ('url', 'name', 'permissions')
