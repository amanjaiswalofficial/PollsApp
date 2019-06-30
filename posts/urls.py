from django.urls import path
from .views import QuestionSet
question_create_view = QuestionSet.as_view({
    'post':'create_question',
})
question_get_view = QuestionSet.as_view({
    'get':'get_question',
})
urlpatterns = [
    path('question/', question_create_view),
    path('question/<int:pk>', question_get_view)
]