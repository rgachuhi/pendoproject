'''
Created on Apr 8, 2015

@author: Raphael
'''
from rest_framework.permissions import IsAdminUser


class IsAdminOrSelf(IsAdminUser):
    """
    Allow access to admin users or the users himself.
    """
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        elif (request.user and type(obj) == type(request.user) and
              obj == request.user):
            return True
        return False