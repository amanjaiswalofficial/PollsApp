from django.contrib.auth.models import AnonymousUser
from rest_framework import status, viewsets
from rest_framework.response import Response
from core.models import Question
from posts.serializers import QuestionSerializer
from django.db.models import Q


class QuestionSet(viewsets.ModelViewSet):

    queryset = Question

    def check_user(self):
        error_message = None
        current_user = None
        if not isinstance(self.request.user, AnonymousUser):
            current_user = self.request.user
        else:
            error_message = {'Error': 'Login With Correct Credentials To Post A Question'}
        return current_user, error_message

    def get_question(self, request, pk):
        question = self.queryset.objects.filter(Q(id=pk))
        if not question:
            return Response({'Error': 'No Question Found'})
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data)
        # return Response({'All':'Well'})

    def create_question(self, request):
        serializer = QuestionSerializer(data=request.data)
        current_user, error_message = QuestionSet.check_user(self)
        if serializer.is_valid() and not error_message:
            self.perform_create(serializer, current_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error = error_message if error_message else serializer.errors
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer, *args):
        current_user = args[0]
        serializer.save(created_by=current_user)
