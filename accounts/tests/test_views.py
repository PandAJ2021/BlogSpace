from django.urls import reverse
from accounts.models import User, SocialLink, UserProfile, OTPCode
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


class SocialLinkViewSetTests(APITestCase):

    def setUp(self):

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
        self.list_url = reverse('accounts:social-link-list')
        self.client.force_authenticate(user=self.user_a)
    
    def test_get_queryset_only_returns_own_links(self):
        SocialLink.objects.create(user=self.user_a, label="Github", link="github.com/user_a")
        SocialLink.objects.create(user=self.user_b, label="Github", link="github.com/user_b")

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['link'], "github.com/user_a")

    def test_max_limit_enforcement(self):
        for i in range(10):
            SocialLink.objects.create(user=self.user_a, label=f"Link {i}", link=f"https://link{i}.com")

        data = {'label': '11th Link', 'link': 'https://link11.com'}
        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Max 10 social links allowed.', str(response.data))
        self.assertEqual(SocialLink.objects.filter(user=self.user_a).count(), 10)
    
    def test_unauthenticated_access_denied(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ListRetrieveProfileView(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='testuser', 
            email='testuser@gmail.com', 
            password='testpassword',
            phone='09123456789'
        )

        self.profile = UserProfile.objects.get(user=self.user)
        self.profile.name = 'Ali'
        self.profile.surname = 'Jalili'
        self.profile.save()

        self.list_url = reverse('accounts:profiles-list') 
        self.detail_url = reverse('accounts:profiles-detail', kwargs={'pk': self.profile.pk})
    
    def test_list_profiles(self):
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Ali")

    def test_retrieve_profile(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Ali")
    
    def test_profile_is_read_only(self):
        post_response = self.client.post(self.list_url, {'name': 'New', 'surname':'New Surname'})
        self.assertEqual(post_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        put_response = self.client.put(self.detail_url, {'name': 'Updated'})
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_retrieve_non_existent_profile(self):
        invalid_url = reverse('accounts:profiles-detail', kwargs={'pk': 1000})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserProfileViewTests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='testuser', 
            email='testuser@gmail.com', 
            password='testpassword',
            phone='09123456789'
        )
        self.other_user = User.objects.create_user(
            username='otheruser', 
            email='testotheruser@gmail.com', 
            password='testpassword',
            phone='09987654321'
        )

        self.profile = UserProfile.objects.get(user=self.user)
        self.profile.name = 'Ali'
        self.profile.surname = 'Jalili'
        self.profile.save()

        self.other_profile = UserProfile.objects.get(user=self.other_user)

        self.me_url = reverse('accounts:profile-me') 
        self.detail_url = reverse('accounts:profile-detail', kwargs={'pk': self.profile.pk})

        self.client.force_authenticate(user=self.user)

    def test_get_my_profile_success(self):
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Ali")
        self.assertEqual(response.data['bio'], self.profile.bio)
    
    def test_update_my_profile_success(self):
        data = {
            'name': 'UpdatedName',
            'surname': 'UpdatedSurname',
            'bio': 'New Bio'
        }
        response = self.client.patch(self.detail_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.name, 'UpdatedName')
    
    def test_delete_my_profile_success(self):
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserProfile.objects.filter(pk=self.profile.pk).exists())

    def test_cannot_delete_others_profile(self):        
        other_url = reverse('accounts:profile-detail', kwargs={'pk': self.other_profile.pk})
        response = self.client.delete(other_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_update_others_profile(self):
        other_url = reverse('accounts:profile-detail', kwargs={'pk': self.other_profile.pk})
        response = self.client.patch(other_url, {'name': 'Ali'})
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SendOTPViewTests(APITestCase):

    def setUp(self):
        self.url = reverse('accounts:send_otp_code') 
        self.phone = "09123456789"
        
        self.user = User.objects.create_user(
            username='user', 
            email='testuser@gmail.com', 
            password='testpassword',
            phone=self.phone
        )

    def test_invalid_phone_format(self):
        data = {'phone': '12345'}
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid phone number')

    def test_user_not_found(self):
        data = {'phone': '09987654321'}
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'There is no user with this number')
    
    def test_send_otp_success(self):
        data = {'phone': self.phone}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Verification code sent')
        self.assertTrue(OTPCode.objects.filter(phone=self.phone).exists())
    
    def test_otp_throttling(self):
        OTPCode.objects.create(phone=self.phone, code=111111)
        
        data = {'phone': self.phone}
        response = self.client.post(self.url, data)
  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Code sent recently, Please wait')

    def test_send_otp_allowed_after_expiration(self):
        from django.utils import timezone
        from datetime import timedelta
        
        expired_time = timezone.now() - timedelta(minutes=3)
        otp = OTPCode.objects.create(phone=self.phone, code=123456)
        
        OTPCode.objects.filter(pk=otp.pk).update(created_at=expired_time)
        
        data = {'phone': self.phone}
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Verification code sent')
