from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from accounts.models import User, SocialLink, UserProfile, OTPCode


class UserModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            phone = "09123456789",
            email = "test@gamil.com",
            username = "testuser",
            password = "passwordtest"
        )
    
    def test_str_returns_username(self):
        self.assertEqual(str(self.user), "testuser")
    
    def test_is_staff_property(self):
        self.user.is_admin = True
        self.assertTrue(self.user.is_staff)
    
    def test_has_perm_always_true(self):
        self.assertTrue(self.user.has_perm("any_perm"))

    def test_has_module_perms_always_true(self):
        self.assertTrue(self.user.has_module_perms("any_app"))


class SocialLinkModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            phone = "09123456789",
            email = "test@gamil.com",
            username = "testuser",
            password = "passwordtest"
        )
        self.social = SocialLink.objects.create(
            user=self.user,
            label="GitHub",
            link="https://github.com/test"
        )

    def test_str_returns_label_and_link(self):
        self.assertEqual(str(self.social), "GitHub : https://github.com/test")
    

class UserProfileModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            phone = "09123456789",
            email = "test@gamil.com",
            username = "testuser",
            password = "passwordtest"
        )

        self.profile, _ = UserProfile.objects.get_or_create(
            user=self.user,
            defaults={"name": "Ali", "surname": "Jalili", "bio": "Hello world", "gender": "male"}
        )

        self.social = SocialLink.objects.create(
            user=self.user,
            label="GitHub",
            link="https://github.com/test"
        )

    def test_str_returns_full_name(self):
        self.assertEqual(str(self.user), "testuser")

    def test_get_social_links_returns_related_links(self):
        links = self.profile.get_social_links
        self.assertEqual(links.count(), 1)
        self.assertEqual(links.first().label, "GitHub")
        self.assertEqual(links.first().link, "https://github.com/test")

    def test_profile_is_linked_to_user(self):
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.user.profile, self.profile)


class OTPCodeModelTests(TestCase):

    def setUp(self):
        self.otp = OTPCode.objects.create(
            phone = "09123456789",
            code = "123456"
        )
    
    def test_str_returns_code_and_phone(self):
        self.assertEqual(str(self.otp), "123456 sent to 09123456789")
    
    def test_is_expired_false_initially(self):
        self.assertFalse(self.otp.is_expired)
    
    def test_is_expired_true_after_3_minutes(self):
        self.otp.created_at = timezone.now() - timedelta(minutes=4)
        self.assertTrue(self.otp.is_expired)