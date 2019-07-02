from django.contrib.auth.models import AnonymousUser, User
import unittest
from rest_framework.test import APIClient


class TestBasic(unittest.TestCase):

    def setUp(self) -> None:
        self.client = APIClient(enforce_csrf_checks=False)
        self.client.login(username='ttn1', password='1234')

    def tearDown(self) -> None:
        self.client.logout()

    def test_get_question_set_status_code(self):
        # request = self.factory.get('/question/')
        response = self.client.get('/question/')
        self.assertEqual(response.status_code, 200)

    def test_get_simple_question_set(self):
        response = self.client.get('/question/')
        self.assertIn('created_by', response.data[0].keys())

    def test_get_question(self):
        response = self.client.get('/question/2')
        self.assertEqual(response.data[0].get('question_text'), 'What color is Sun?')

    # def test_post_simple_question(self):
    #     # response = QuestionCreateGetSet.as_view({'post': 'create_question'})(request)
    #     # response = QuestionCreateGetSet().as_view()(request)
    #     # response = QuestionCreateGetSet().get_question_set(request)
    #     response = self.client.post('/question/',{'question_text': 'Is This A Question?'})
    #     self.assertEqual(response.data.get('question_text'),'Is This A Question?')

    def test_update_question_success(self):
        question = {'question_text': 'What Color Is Moon?'}
        response = self.client.put('/question/2', data=question)
        self.assertIn(question['question_text'], response.data.values())

    def test_update_question_failure(self):
        self.client.login(username='ttn2', password='1234')
        response = self.client.put('/question/2', {'question_text': 'How Many Days In A Week?'})
        self.assertNotEqual(response.status_code, 200)

    # def test_delete_question_success(self):
    #     response = self.client.delete('/question/1')
    #     import pdb;
    #     pdb.set_trace()
    #     self.assertEqual(response.data['Message'], 'Question Deleted Successfully')