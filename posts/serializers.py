from rest_framework import serializers
from core.models import Question, Choice


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('created_by', 'question_text',)
        extra_kwargs = {'created_by': {'required': False}}

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('question','choice_text',)
