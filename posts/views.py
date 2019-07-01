from django.contrib.auth.models import AnonymousUser
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from core.models import Question, Choice
from posts.serializers import QuestionSerializer, ChoiceSerializer
from django.db.models import Q
from .error_messages import *
from .permissions import IsOwnerOrReadOnly, DidUserCreateQuestion


class QuestionCreateGetSet(viewsets.ModelViewSet):

    queryset = Question
    serializer_class = QuestionSerializer

    def get_question_set(self, request):
        question_set = self.queryset.objects.all()
        serializer = QuestionSerializer(question_set, many=True)
        return Response(serializer.data)

    def create_question(self, request):
        serializer = QuestionSerializer(data=request.data)
        current_user, error_message = check_user(self.request.user)
        if serializer.is_valid() and not error_message:
            self.perform_create(serializer, current_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error = error_message if error_message else serializer.errors
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer, *args):
        current_user = args[0]
        serializer.save(created_by=current_user)


class QuestionViewUpdateSet(viewsets.ModelViewSet):

    queryset = Question
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    def get_question(self, request, pk):
        current_question, object_exists = self.check_valid_object(pk)
        if object_exists:
            serializer = QuestionSerializer(current_question, many=True)
            return Response(serializer.data)
        return Response(NO_QUESTION_FOUND_ERROR)

    def update_question(self, request, pk):
        objects = self.queryset.objects.filter(Q(id=pk))
        current_object, object_exists = self.check_valid_object(pk)
        if object_exists:
            object_instance = objects[0]
            self.check_object_permissions(request, object_instance)
            self.update(object_instance, request.data)
            serializer = QuestionSerializer(object_instance)
            return Response(serializer.data)
        return Response(NO_QUESTION_FOUND_ERROR)

    def delete_question(self, request, pk):
        current_object, object_exists = self.check_valid_object(pk)
        if object_exists:
            self.queryset.objects.filter(pk=pk).delete()
            return Response(DELETE_SUCCESSFUL_MESSAGE)
        return Response(NO_QUESTION_FOUND_ERROR)

    def update(self, instance, validated_data):
        for field in validated_data.keys():
            setattr(instance, field, validated_data.get(field))
        return instance


    # def delete(self, pk):
    #     self.queryset.objects.filter(pk=pk).delete()
    #     # return self.queryset


class ChoiceCreateGetSet(viewsets.ModelViewSet):
    queryset = Choice
    serializer_class = ChoiceSerializer
    permission_classes = (DidUserCreateQuestion, )

    def get_choice_set(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
            choice_set = self.queryset.objects.filter(question=question)
            serializer = ChoiceSerializer(choice_set, many=True)
            return Response(serializer.data)
        except Question.DoesNotExist:
            return Response([{'Error':'No Such Question Exist'}])

    def create_choice(self, request):
        serializer = ChoiceSerializer(data=request.data)
        current_user, error_message = check_user(self.request.user)
        if serializer.is_valid() and not error_message:
            object_instance = request.data.get('question')
            self.check_object_permissions(request, object_instance)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error = error_message if error_message else serializer.errors
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer, *args):
        serializer.save()

    def get_question(self, pk):
        pass

class ChoiceUpdateDeleteView(viewsets.ModelViewSet):
    queryset = Choice
    serializer_class = ChoiceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, DidUserCreateQuestion,)

    def delete_choice(self, request, question_pk, choice_pk):
        current_object, object_exists = check_valid_object(self.queryset, question=question_pk, id=choice_pk)
        if object_exists:
            self.check_object_permissions(request, current_object[0].question.id)
            self.queryset.objects.filter(pk=current_object[0].pk).delete()
            return Response(DELETE_SUCCESSFUL_MESSAGE)
        return Response(NO_CHOICE_FOUND_ERROR)

def check_user(user):
    error_message = None
    current_user = None
    if not isinstance(user, AnonymousUser):
        current_user = user
    else:
        error_message = INVALID_CREDENTIAL_ERROR
    return current_user, error_message

def check_valid_object(queryset, **kwargs):
    objects = queryset.objects.filter(Q(**kwargs))
    if not objects:
        return None, False
    return objects, True

