from django.urls import path, re_path
from .views import QuestionCreateGetSet, QuestionViewUpdateSet,ChoiceCreateUpdateDeleteView

question_create_set_view = QuestionCreateGetSet.as_view({
    'get': 'get_question_set',
    'post':'create_question',
})
question_get_view = QuestionViewUpdateSet.as_view({
    'get':'get_question',
    'put': 'update_question',
    'delete': 'delete_question',
})
choices_post_put_delete_view = ChoiceCreateUpdateDeleteView.as_view({
    'post':'create_choice',
    'put': 'update_choice',
    'delete': 'delete_choice'
})
choices_get_view = ChoiceCreateUpdateDeleteView.as_view({
    'get':'get_choice_set'
})

urlpatterns = [
    path('question/', question_create_set_view),
    path('question/<int:pk>', question_get_view),
    path('choice/', choices_post_put_delete_view),
    path('choice/question/<int:pk>', choices_get_view),
    #re_path(r'^choic', choices_get_view),

]