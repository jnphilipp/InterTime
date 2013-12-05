from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
import re

class ViewsTestCase(TestCase):
	def setUp(self):
		self.client = Client()

	def test_index_works(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

	def test_reisgter_works(self):
		response = self.client.get('/user/register/')
		match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+?)"', response.content)
		self.assertIsNone(match)
		if match:
			response = self.client.post('/user/register/', {'id_username': 'john', 'id_password1': 'smith', 'id_password2': 'smith', 'csrfmiddlewaretoken': match.group(1)})
			user = User.objects.filter(username='john').count()
			self.assertEqual(user, 1)