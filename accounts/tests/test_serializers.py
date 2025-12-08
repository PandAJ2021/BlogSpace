from django.test import TestCase
from accounts.models import User
from accounts.serializers import UserRegisterSerializer


class UserRegisterSerializerTests(TestCase):

    def setUp(self):
        self.valid_data = {
            "phone":"09123456789",
            "email":"test@gmail.com",
            "username":"testuser",
            "password":"testpassword",
            "password2":"testpassword"
        }
    
    def test_serializer_valid_data_creates_user(self):
        serializer = UserRegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.phone, "09123456789")
        self.assertEqual(user.email, "test@gmail.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpassword"))
    
    def test_invalid_phone(self):
        data = self.valid_data.copy()
        data["phone"] = "0123456789"
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)
    
    def test_passwords_must_match(self):
        data = self.valid_data.copy()
        data["password2"] = "differentpassword"
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
    
    def test_duplicate_username_not_allowed(self):

        User.objects.create_user(
            phone="09987654321",
            email="newtest@gmail.com",
            username="testuser",
            password="testpassword"
        )
        serializer = UserRegisterSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_duplicate_email_not_allowed(self):

        User.objects.create_user(
            phone="09987654321",
            email="test@gmail.com",
            username="newtestuser",
            password="testpassword"
        )

        serializer = UserRegisterSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)


