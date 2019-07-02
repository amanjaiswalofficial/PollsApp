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
        """Returns set of all questions"""
        question_set = self.queryset.objects.all()
        serializer = QuestionSerializer(question_set, many=True)
        return Response(serializer.data)

    def create_question(self, request):
        """Creates a question with currently logged in user"""
        serializer = QuestionSerializer(data=request.data)
        current_user, error_message = check_user(self.request.user)
        if serializer.is_valid() and not error_message:
            self.perform_create(serializer, current_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error = error_message if error_message else serializer.errors
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer, *args):
        """Create instance of question after getting current user"""
        current_user = args[0]
        serializer.save(created_by=current_user)


class QuestionViewUpdateSet(viewsets.ModelViewSet):

    queryset = Question
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    def get_question(self, request, pk):
        """Return a particular question based on id provided"""
        current_question, object_exists = check_valid_object(self.queryset, pk=pk)
        if object_exists:
            serializer = QuestionSerializer(current_question, many=True)
            return Response(serializer.data)
        return Response(NO_QUESTION_FOUND_ERROR)

    def update_question(self, request, pk):
        """Update a particular question's text after authenticating the logged in user"""
        objects = self.queryset.objects.filter(Q(id=pk))
        current_object, object_exists = check_valid_object(self.queryset, id=pk)
        if object_exists:
            object_instance = objects[0]
            self.check_object_permissions(request, object_instance)
            self.update(object_instance, request.data)
            serializer = QuestionSerializer(object_instance)
            return Response(serializer.data)
        return Response(NO_QUESTION_FOUND_ERROR)

    def delete_question(self, request, pk):
        """Delete a question after checking if it exists and whether current user is authenticated"""
        current_object, object_exists = check_valid_object(self.queryset, pk=pk)
        if object_exists:
            self.queryset.objects.filter(pk=pk).delete()
            return Response(DELETE_SUCCESSFUL_MESSAGE)
        return Response(NO_QUESTION_FOUND_ERROR)

    def update(self, instance, validated_data):
        """Update the instance with validated data provided"""
        for field in validated_data.keys():
            setattr(instance, field, validated_data.get(field))
        return instance


class ChoiceCreateUpdateDeleteView(viewsets.ModelViewSet):
    queryset = Choice
    serializer_class = ChoiceSerializer
    permission_classes = (DidUserCreateQuestion, )

    def get_choice_set(self, request, pk):
        """Return all choices related to a question based on pk provided"""
        try:
            question = Question.objects.get(pk=pk)
            choice_set = self.queryset.objects.filter(question=question)
            if choice_set:
                serializer = ChoiceSerializer(choice_set, many=True)
                response = serializer.data
            else:
                response = NO_CHOICE_FOUND_ERROR
            return Response(response)
        except Question.DoesNotExist:
            return Response([{'Error':'No Such Question Exist'}])

    def create_choice(self, request):
        """Create a choice for a question based on it's id provided and authenticating the user"""
        filters = {}
        serializer = ChoiceSerializer(data=request.data)
        current_user, error_message = check_user(self.request.user)
        if serializer.is_valid() and not error_message:
            object_instance = request.data.get('question', None)
            self.check_object_permissions(request, object_instance)
            filters['question'] = object_instance
            filters['choice_text'] = request.data.get('choice_text', None)
            current_object, object_exists = check_valid_object(self.queryset, **filters)
            if object_exists:
                self.perform_create(serializer)
                response = serializer.data
                response_status = status.HTTP_201_CREATED
            else:
                response = INVALID_ENTRY_ERROR
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            response = error_message if error_message else serializer.errors
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(response, response_status)

    def update_choice(self, request):
        """Updates choice for a question based on question and choice_id provided"""
        filters = {}
        serializer = ChoiceSerializer(data=request.data)
        current_user, error_message = check_user(self.request.user)
        if serializer.is_valid() and not error_message:
            filters['id'] = int(request.data.get('id'))
            filters['question'], object_exists = self.get_question(request.data.get('question'))
            current_object, object_exists = check_valid_object(self.queryset, **filters)
            filters['choice_text'] = request.data.get('choice_text')
            if object_exists:
                self.check_object_permissions(request, filters['question'].id)
                self.update(current_object[0], filters)
                response = serializer.data
                response_status = status.HTTP_200_OK
            else:
                response = NO_CHOICE_FOUND_ERROR
                response_status = status.HTTP_400_BAD_REQUEST
            return Response(response, response_status)
        else:
            error = error_message if error_message else serializer.errors
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def update(self, instance, validated_data):
        """Update the instance with validated data"""
        for field in validated_data.keys():
            setattr(instance, field, validated_data.get(field))
        instance.save()
        return instance

    def delete_choice(self, request):
        """Delete a choice for a question based on question and choice text provided"""
        filters = {}
        current_user, error_message = check_user(request.user)
        if error_message:
            response = error_message
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            filters['question_id'] = request.data.get('question')
            filters['choice_text'] = request.data.get('choice_text')
            current_choice, object_exists = check_valid_object(self.queryset, **filters)
            if object_exists:
                question_with_choice = current_choice[0].question
                self.check_object_permissions(request, question_with_choice.id)
                self.queryset.objects.filter(**filters).delete()
                response = CHOICE_DELETE_SUCCESSFUL_MESSAGE
                response_status = status.HTTP_200_OK
            else:
                response = NO_CHOICE_FOUND_ERROR
                response_status = status.HTTP_400_BAD_REQUEST
        return Response(response, response_status)
        #RETURN REMAINING CHOICE

    def perform_create(self, serializer, *args):
        """Create an instance"""
        serializer.save()

    def get_question(self, pk):
        """Check if question exists, return False if it doeesn't"""
        question = None
        no_question_exist = False
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            no_question_exist = True
        return question, no_question_exist


def check_user(user):
    """Check if a user is logged in or not, else return error"""
    error_message = None
    current_user = None
    if not isinstance(user, AnonymousUser):
        current_user = user
    else:
        error_message = INVALID_CREDENTIAL_ERROR
    return current_user, error_message


def check_valid_object(queryset, **kwargs):
    """Check if provided filters match any object or objects, return a query_dict"""
    objects = queryset.objects.filter(Q(**kwargs))
    if not objects:
        return None, False
    return objects, True

