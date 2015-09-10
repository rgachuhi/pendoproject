from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User
from django.template.defaultfilters import default
import uuid

    
class Match(models.Model):
    LIKED = 'liked'
    MATCHED = 'matched'
    REJECTED = 'rejected'
    CHAT = 'chat'
    STATUS = (
        (LIKED, 'liked'),
        (MATCHED, 'matched'),
        (REJECTED, 'rejected'),
        (CHAT, 'chat'),
    )
    #users = models.ManyToManyField(User)
    #source = models.EmailField(max_length=255)
    source   = models.ForeignKey(User, related_name = 'source_user')
    target = models.ForeignKey(User, related_name = 'target_user')
    status = models.CharField(max_length=20, choices=STATUS, default=LIKED)
    created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    
class Preferences(models.Model):
    FEMALE = 'f'
    MALE = 'm'
    BOTH = 'b'
    GENDER_PREF = (
        (FEMALE, 'female'),
        (MALE, 'male'),
        (BOTH, 'both'),
    )
    user = models.OneToOneField(User, primary_key=True)
    min_age = models.IntegerField(default=20, validators=[MaxValueValidator(100), MinValueValidator(14)])
    max_age = models.IntegerField(default=50, validators=[MaxValueValidator(100), MinValueValidator(15)])
    gender_pref = models.CharField(max_length=1, choices=GENDER_PREF, default=FEMALE)
    distance = models.IntegerField(default=30, validators=[MaxValueValidator(100), MinValueValidator(10)])
    # hide from discovery
    hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

class ChatStream(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #users = models.ManyToManyField(User)
    user1   = models.ForeignKey(User, related_name = 'user1_user')
    user2 = models.ForeignKey(User, related_name = 'user2_user')
    created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    stream = models.ForeignKey(ChatStream)
    sender   = models.ForeignKey(User, related_name = 'sender_user')
    receiver = models.ForeignKey(User, related_name = 'receiver_user')
    #source = models.EmailField(max_length=255)
    #target = models.EmailField(max_length=255)
    message = models.CharField(max_length=600)
    created = models.DateTimeField(auto_now_add=True)
    