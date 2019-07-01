from django.urls import path, re_path
from .views import QuestionCreateGetSet, QuestionViewUpdateSet, ChoiceCreateGetSet, ChoiceUpdateDeleteView

question_create_set_view = QuestionCreateGetSet.as_view({
    'get': 'get_question_set',
    'post':'create_question',
})
choices_post_view = ChoiceCreateGetSet.as_view({
    'post':'create_choice'
})
choices_get_view = ChoiceCreateGetSet.as_view({
    'get':'get_choice_set'
})
question_get_view = QuestionViewUpdateSet.as_view({
    'get':'get_question',
    'put': 'update_question',
    'delete': 'delete_question',
})
choice_update_delete_view = ChoiceUpdateDeleteView.as_view({
    'delete': 'delete_choice'
})

urlpatterns = [
    path('question/', question_create_set_view),
    path('question/<int:pk>', question_get_view),
    #re_path(r'^choic', choices_get_view),
    path('choice/', choices_post_view),
    path('choices/question/<int:pk>', choices_get_view),
    path('choice/question/<int:question_pk>/<int:choice_pk>', choice_update_delete_view)

]