from rest_framework import serializers
from core.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('created_by', 'question_text',)
        extra_kwargs = {'created_by': {'required': False}}
