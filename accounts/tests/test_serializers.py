from django.test import TestCase
from accounts.models import User, SocialLink
from accounts.serializers import UserRegisterSerializer, AdminUserSerializer, SocialLinkSerializer


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


class AdminUserSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            phone="09987654321",
            email="test@gmail.com",
            username="testuser",
            password="testpassword"
        )

    def test_update_without_password(self):
        data = {
            "phone":"09987654321",
            "email":"newtest@gmail.com",
            "username":"newtestuser",
            "is_active":False,
            "is_admin":True
        }
        serializer = AdminUserSerializer(data=data, instance=self.user, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        update_user = serializer.save()
        self.assertEqual(update_user.phone, "09987654321")
        self.assertEqual(update_user.email, "newtest@gmail.com")
        self.assertEqual(update_user.username, "newtestuser")
        self.assertTrue(update_user.is_admin)
        self.assertFalse(update_user.is_active)
        self.assertTrue(update_user.check_password("testpassword"))
    
    def test_update_with_password(self):
        data = {
            "password":"newtestpassword",
        }
        serializer = AdminUserSerializer(data=data, instance=self.user, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        update_user = serializer.save()
        self.assertFalse(update_user.check_password("testpassword"))

    
    def test_invalid_phone_number(self):
        data = {
            "phone":"08123456789",
        }
        serializer = AdminUserSerializer(data=data, instance=self.user, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)

    def test_duplicate_username_not_allowed(self):
        User.objects.create_user(
            phone="09999999999",
            email="othertest@gmail.com",
            username="duplicatetestuser",
            password="testpassword"
        )

        data = {
            "username":"duplicatetestuser",
        }
        serializer = AdminUserSerializer(data=data, instance=self.user, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_duplicate_email_not_allowed(self):
        User.objects.create_user(
            phone="09999999999",
            email="duplicatetest@gmail.com",
            username="othertetestuser",
            password="testpassword"
        )

        data = {
            "email":"duplicatetest@gmail.com",
        }
        serializer = AdminUserSerializer(data=data, instance=self.user, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)


class SocialLinkSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone="09987654321",
            email="newtest@gmail.com",
            username="testuser",
            password="testpassword"
        )

    def test_serializer_valid_data(self):
        data = {
            "label":"GitHub",
            "link":"https://github.com/example"
        }
        serializer = SocialLinkSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        obj = serializer.save(user=self.user)
        self.assertIsInstance(obj, SocialLink)
        self.assertEqual(obj.label, "GitHub")
        self.assertEqual(obj.link, "https://github.com/example")