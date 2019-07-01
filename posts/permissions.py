from rest_framework import permissions
from core.models import Question

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

class DidUserCreateQuestion(permissions.BasePermission):

    def has_object_permission(self, request, view, id):
        current_question = Question.objects.get(pk=id)
        return current_question.created_by == request.user