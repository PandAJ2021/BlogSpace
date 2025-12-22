from django.urls import reverse
from accounts.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


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


class AdminUserViewSetTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin_staff', 
            email='admin@gmail.com', 
            password='testpassword',
            phone='09123456789'
        )
        
        self.regular_user = User.objects.create_user(
            username='regular_user', 
            email='regular@gmail.com', 
            password='testpassword',
            phone='09987654321'
        )

        self.list_url = reverse('accounts:admin-list')
        self.detail_url = reverse('accounts:admin-detail', kwargs={'pk': self.regular_user.pk})

    def test_list_users_as_admin_allowed(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_users_as_regular_user_forbidden(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_anonymous_unauthorized(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'username': 'updated_name', 'phone': '09100000000'}
        response = self.client.patch(self.detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.username, 'updated_name')

    def test_soft_delete_execution(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.regular_user.refresh_from_db()
        self.assertFalse(self.regular_user.is_active, "User should be deactivated")
        # user record should exist
        self.assertTrue(User.objects.filter(pk=self.regular_user.pk).exists())

    def test_update_user_as_regular_user_forbidden(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {'username': 'updated_name', 'phone': '09100000000'}
        
        response = self.client.patch(self.detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.username, 'regular_user')


class UserLogoutViewTests(APITestCase):

    def setUp(self):
        self.url = reverse('accounts:user_logout')
        
        self.user_a = User.objects.create_user(
            phone="09987654321",
            email="user_a@gmail.com",
            username="testuser_a",
            password="testpassword"
        )
        self.user_b = User.objects.create_user(
            phone="09123456789",
            email="user_b@gmail.com",
            username="testuser_b",
            password="testpassword"
        )

    def test_logout_success(self):
        refresh = RefreshToken.for_user(self.user_a)
        data = {'refresh': str(refresh)}
        
        self.client.force_authenticate(user=self.user_a)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        
        # Verify the token is actually blacklisted
        # SimpleJWT raises TokenError if I try to refresh a blacklisted token
        with self.assertRaises(Exception):
            refresh.check_blacklist()

    def test_logout_with_others_token_forbidden(self):
        refresh_b = RefreshToken.for_user(self.user_b)
        data = {'refresh': str(refresh_b)}
        
        self.client.force_authenticate(user=self.user_a)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'Token does not belongs to authentication user')

    def test_logout_invalid_token(self):
        self.client.force_authenticate(user=self.user_a)
        data = {'refresh': 'this-is-not-a-valid-token'}
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    