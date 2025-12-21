from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from accounts.admin import UserAdmin, OTPCodeAdmin, UserProfileAdmin
from accounts.models import OTPCode, UserProfile

User = get_user_model()

class UserAdminTest(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.user_admin = UserAdmin(User, self.site)
    
    def test_admin_registration(self):
        """Verify that the User model is registered with UserAdmin."""
        from django.contrib import admin
        # Check if User is registered in the actual default admin site
        self.assertIsInstance(admin.site._registry.get(User), UserAdmin)

    def test_ordering(self):
        self.assertEqual(self.user_admin.ordering, ('username',))

    def test_list_display(self):
        expected_list_display = ('phone', 'email', 'username', 'is_admin', 'is_active')
        self.assertEqual(self.user_admin.list_display, expected_list_display)

    def test_list_filter(self):
        expected_list_filter = ('is_active', 'is_admin')
        self.assertEqual(self.user_admin.list_filter, expected_list_filter)
    
    def test_search_fields(self):
        expected_search_fields = ('phone', 'email', 'username')
        self.assertEqual(self.user_admin.search_fields, expected_search_fields)

    def test_add_fieldsets_structure(self):
        add_fieldsets = self.user_admin.add_fieldsets
        expected_fields = ('phone', 'email', 'username', 'password', 'is_admin', 'is_active')
        fields_in_admin = add_fieldsets[0][1]['fields']
        self.assertEqual(fields_in_admin, expected_fields)


class OTPCodeAdminTest(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.admin = OTPCodeAdmin(OTPCode, self.site)

    def test_admin_ordering(self):
        self.assertEqual(self.admin.ordering, ('-created_at',))

    def test_admin_list_display(self):
        expected_display = ('phone', 'code', 'created_at', 'is_expired')
        self.assertEqual(self.admin.list_display, expected_display)

    def test_admin_search_fields(self):
        self.assertEqual(self.admin.search_fields, ('phone',))


class UserProfileAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = UserProfileAdmin(UserProfile, self.site)
        self.user = User.objects.create_user(
            phone = "09123456789",
            email = "test@gamil.com",
            username = "testuser",
            password = "passwordtest"
        )
        self.profile = UserProfile.objects.get(user=self.user)

    def test_admin_ordering(self):
        self.assertEqual(self.admin.ordering, ('-created_at',))

    def test_admin_list_display(self):
        expected_display = ('user', 'name', 'surname')
        self.assertEqual(self.admin.list_display, expected_display)

    def test_admin_search_fields(self):
        expected_search = ('name', 'surname')
        self.assertEqual(self.admin.search_fields, expected_search)

    def test_user_link_resolution(self):
        """
        Since 'user' is a ForeignKey, this ensures the admin can 
        access the related user string representation without crashing.
        """
        display_value = self.profile.user.__str__()
        self.assertEqual(display_value, 'testuser')