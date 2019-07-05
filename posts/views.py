from django.contrib.auth.models import AnonymousUser
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from core.models import Question, Choice
from posts.serializers import QuestionSerializer, ChoiceSerializer
from django.db.models import Q
from .error_messages import *
from .permissions import IsOwnerOrReadOnly, DidUserCreateQuestion
from .serializer_action import *


class QuestionCreateGetSet(viewsets.ModelViewSet):

    queryset = Question
    serializer_class = QuestionSerializer

    def get_question_set(self, request):
        """Returns set of all questions"""
        response, response_status_code = perform_action(action_type='get_question_set',
                                                        current_queryset=self.queryset)
        response = QuestionSerializer(response, many=True).data
        return Response(response, response_status_code)

    def create_question(self, request):
        """Creates a question with currently logged in user"""
        serializer = QuestionSerializer(data=request.data)
        response, response_status_code = perform_action(action_type='create_question',
                                                         current_user=request.user,
                                                         serializer=serializer)
        return Response(response, response_status_code)


class QuestionViewUpdateSet(viewsets.ModelViewSet):

    queryset = Question
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    custom_permission = (IsOwnerOrReadOnly, )

    def get_question(self, request, pk):
        """Return a particular question based on id provided"""
        response, response_status_code = perform_action(action_type='get_question',
                                                        current_queryset=self.queryset,
                                                        pk=pk)
        if not response_status_code == status.HTTP_400_BAD_REQUEST:
            response = QuestionSerializer(response, many=True).data
        return Response(response, response_status_code)

    def update_question(self, request, pk):
        """Update a particular question's text after authenticating the logged in user"""
        request_data = request.data
        response, response_status_code = perform_action(action_type='update_question',
                                                        current_queryset=self.queryset,
                                                        current_user=self.request.user,
                                                        permissions=self.custom_permission,
                                                        request_data=request_data,
                                                        pk=pk)
        return Response(response, response_status_code)

    def delete_question(self, request, pk):
        """Delete a question after checking if it exists and whether current user is authenticated"""
        response, response_status_code = perform_action(action_type='delete_question',
                                                        current_queryset=self.queryset,
                                                        current_user=self.request.user,
                                                        permissions=self.custom_permission,
                                                        pk=pk)
        return Response(response, response_status_code)

    def update(self, instance, validated_data):
        """Update the instance with validated data provided"""
        for field in validated_data.keys():
            setattr(instance, field, validated_data.get(field))
        return instance


class ChoiceCreateUpdateDeleteView(viewsets.ModelViewSet):
    _model = Choice
    queryset = Choice
    _other_models = Question
    serializer_class = ChoiceSerializer
    custom_permission = (DidUserCreateQuestion, )

    def get_choice_set(self, request, pk):
        """Return all choices related to a question based on pk provided"""
        response, response_status_code = perform_action(action_type='get_choice_set',
                                                        current_model=self._model,
                                                        other_model=self._other_models,
                                                        pk=pk)
        if not response_status_code == status.HTTP_400_BAD_REQUEST:
            response = ChoiceSerializer(response, many=True).data
        return Response(response, response_status_code)
        # try:
        #     question = Question.objects.get(pk=pk)
        #     choice_set = self.queryset.objects.filter(question=question)
        #     if choice_set:
        #         serializer = ChoiceSerializer(choice_set, many=True)
        #         response = serializer.data
        #     else:
        #         response = NO_CHOICE_FOUND_ERROR
        #     return Response(response)
        # except Question.DoesNotExist:
        #     return Response([{'Error':'No Such Question Exist'}])

    def create_choice(self, request):
        """Create a choice for a question based on it's id provided and authenticating the user"""
        serializer = ChoiceSerializer(data=request.data)
        response, response_status_code = perform_action(action_type='create_choice',
                                                        current_model=[self._model, self._other_models],
                                                        current_user=self.request.user,
                                                        permissions=self.custom_permission,
                                                        serializer=serializer,
                                                        request_data=request.data)
        if response_status_code == status.HTTP_201_CREATED:
            response = serializer.data
        return Response(response, response_status_code)

    def update_choice(self, request):
        """Updates choice for a question based on question and choice_id provided"""

        response, response_status_code = perform_action(action_type='update_choice',
                                                        current_model=self._model,
                                                        other_model=self._other_models,
                                                        current_user=self.request.user,
                                                        permissions=self.custom_permission,
                                                        request_data=request.data)
        return Response(response, response_status_code)

    def delete_choice(self, request):
        """Delete a choice for a question based on question and choice text provided"""
        response, response_status_code = perform_action(action_type='delete_choice',
                                                        current_model=self._model,
                                                        other_model=self._other_models,
                                                        current_user=self.request.user,
                                                        permissions=self.custom_permission,
                                                        request_data=request.data)

        return Response(response, response_status_code)

