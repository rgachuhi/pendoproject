from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAdminUser, AllowAny

from .serializers import UserSerializer, PasswordSerializer, GroupSerializer
#from .permissions import IsAdminOrSelf

from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
import logging
from django.contrib.gis.geos.factory import fromstr

# Get an instance of a logger
logger = logging.getLogger('flirtupendo')


User = get_user_model()
    
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    To set a password, POST a `password` on the `/set_password/` url.
    To set a unusuable password, set `!` as a password.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @detail_route(methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.DATA)
        if serializer.is_valid():
            password = self.request.DATA['password']
            if password == '!':
                user.set_unusable_password()
            else:
                user.set_password(password)
                user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
            