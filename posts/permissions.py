from rest_framework import permissions
from core.models import Question

class AuthenticationError(Exception):
    pass

class IsOwnerOrReadOnly(permissions.BasePermission):

    # def has_object_permission(self, request, view, obj):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     return obj.created_by == request.user
    def has_object_permission(user, object):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        #return obj.created_by == request.user
        return object.created_by == user

class DidUserCreateQuestion(permissions.BasePermission):

    def has_object_permission(user, object):
        #current_question = Question.objects.get(pk=id)
        return object.created_by == user