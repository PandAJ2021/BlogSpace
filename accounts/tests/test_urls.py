from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts import views


class TestAccountsURLs(SimpleTestCase):

    def test_register_url_resolves(self):
        url = reverse('accounts:user_register')
        self.assertEqual(resolve(url).func.view_class, views.UserRegisterView)
    
    def test_logout_url_resolves(self):
        url = reverse('accounts:user_logout')
        self.assertEqual(resolve(url).func.view_class, views.UserLogoutView)
    
    def test_send_otp_url_resolves(self):
        url = reverse('accounts:send_otp_code')
        self.assertEqual(resolve(url).func.view_class, views.SendOTPView)

    def test_token_by_otp_url_resolves(self):
        url = reverse('accounts:token_by_otp')
        self.assertEqual(resolve(url).func.view_class, views.OTPLoginView)
    
    def test_admin_router_resolves(self):
        #admin_list for create and list
        url = reverse('accounts:admin-list')
        self.assertEqual(resolve(url).func.cls, views.AdminUserViewSet)
    
    def test_admin_router_detail_resolves(self):
        #admin_detail for retrieve, destroy and update
        url = reverse('accounts:admin-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, views.AdminUserViewSet)

    def test_profiles_router_resolves(self):
        url = reverse('accounts:profiles-list')
        self.assertEqual(resolve(url).func.cls, views.ListRetrieveProfileView)
    
    def test_profiles_router_detail_resolves(self):
        url = reverse('accounts:profiles-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, views.ListRetrieveProfileView)
    
    def test_profile_router_detail_resolves(self):
        url = reverse('accounts:profile-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, views.UserProfileView)

    def test_profile_router_me_resolves(self):
        url = reverse('accounts:profile-me')
        self.assertEqual(resolve(url).func.cls, views.UserProfileView)

    def test_social_link_router_resolves(self):
        url = reverse('accounts:social-link-list')
        self.assertEqual(resolve(url).func.cls, views.SocialLinkViewSet)
    
    def test_social_link_router_detail_resolves(self):
        url = reverse('accounts:social-link-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, views.SocialLinkViewSet)