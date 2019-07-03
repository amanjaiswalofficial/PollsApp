from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient


class TestBasic(TestCase):

    def setUp(self) -> None:
        self.client = APIClient(enforce_csrf_checks=False)
        User.objects.create_user(username='ttn1',password='1234')
        self.client.login(username='ttn1', password='1234')
        self.client.post('/question/', {'question_text': 'This Is Question 1?'})
        self.client.post('/question/', {'question_text': 'This Is Question 2?'})
        self.client.post('/question/', {'question_text': 'This Is Question 3?'})
        self.client.post('/question/', {'question_text': 'This Is Question 4?'})
        self.client.post('/question/', {'question_text': 'This Is Question 5?'})

    def tearDown(self) -> None:
        self.client.logout()

    def test_post_simple_question(self):
        # response = QuestionCreateGetSet.as_view({'post': 'create_question'})(request)
        # response = QuestionCreateGetSet().as_view()(request)
        # response = QuestionCreateGetSet().get_question_set(request)
        response = self.client.post('/question/', {'question_text': 'Is This A Question?'})
        self.assertEqual(response.status_code, 201)

    def test_get_question_set_status_code(self):
        response = self.client.get('/question/')
        self.assertEqual(response.status_code, 200)

    def test_get_question(self):
        response = self.client.get('/question/2')
        self.assertEqual(response.data[0].get('question_text'), 'This Is Question 2?')

    def test_delete_question_success(self):
        response = self.client.delete('/question/1')
        #self.assertNotEqual(response.data[0]['Error'], 'No Question Found')
        self.assertNotEqual(response.status_code, 400)

    def test_create_choice_for_question_success(self):
        response = self.client.post('/choice/', {'question': '1', 'choice_text': 'Choice 1 for question 1'})
        response = self.client.get('/choice/question/1')
        self.assertEqual(response.status_code, 200)

    def test_create_choice_for_question_failure(self):
        self.user = AnonymousUser
        response = self.client.post('/choice/', {'question': '1', 'choice_text': 'Choice 1 for question 1'})
        response = self.client.get('/choice/question/1')
        self.assertEqual(response.data[0]['Error'], 'No Choice Found')

    def test_update_question_success(self):
        question = {'question_text': 'What Color Is Moon?'}
        response = self.client.put('/question/2', data=question)
        self.assertEqual(response.status_code, 200)

    def test_update_question_failure_for_auth_failure(self):
        self.user = AnonymousUser
        question = {'question_text': 'What Color Is Moon?'}
        response = self.client.put('/question/2', data=question)
        self.assertNotEqual(response.status_code, 200)