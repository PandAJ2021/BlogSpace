from django.urls import reverse
from accounts.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class UserRegisterViewTests(APITestCase):

    def setUp(self):
        self.url = reverse('accounts:user_register')
        self.valid_data = {
            'phone': '09123456789',
            'email': 'test@gmail.com',
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword'
        }

    def test_user_registration_success(self):
        response = self.client.post(self.url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        #passwords must not return in response
        self.assertNotIn('password', response.data)
        self.assertNotIn('password2', response.data)

    def test_registration_logic_failure(self):
        data = self.valid_data.copy()
        data['password2'] = 'mismatch'
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_registration_schema_failure(self):
        response = self.client.post(self.url, {}) # Empty dict
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

