from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now=True)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)