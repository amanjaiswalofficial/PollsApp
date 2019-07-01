from django.urls import path
from .views import QuestionCreateGetSet, QuestionViewUpdateSet
question_create_set_view = QuestionCreateGetSet.as_view({
    'get': 'get_question_set',
    'post':'create_question',
})
question_get_view = QuestionViewUpdateSet.as_view({
    'get':'get_question',
    'put': 'update_question',
    'delete': 'delete_question',
})
urlpatterns = [
    path('question/', question_create_set_view),
    path('question/<int:pk>', question_get_view)
]