from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.utils import timezone
from datetime import timedelta


class User(AbstractBaseUser):
    phone = models.CharField(verbose_name='phone number', unique=True, max_length=11)
    email = models.EmailField(verbose_name='Email address', unique=True, max_length=255)
    username = models.CharField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager() 

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email','username',]

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    

class SocialLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_links')
    label = models.CharField(max_length=55)
    link = models.URLField()

    def __str__(self):
        return f'{self.label} : {self.link}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(verbose_name='First Name', max_length=55, null=True, blank=True)
    surname = models.CharField(verbose_name='Last Name', max_length=55, null=True, blank=True)
    picture = models.ImageField(verbose_name='Profile Picture', upload_to='accounts/', null=True, blank=True)
    bio = models.TextField(verbose_name='Biography', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(choices=[
        ('male','male'),
        ('female','female'),
        ('other','other')],
        null= True, blank=True)
    
    @property
    def get_social_links(self):
        return self.user.social_links.all()
    
    def __str__(self):
        return f'{self.name} {self.surname}'


class OTPCode(models.Model):
    phone = models.CharField(verbose_name='Phone Number', max_length=11)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.code} sent to {self.phone}'
    
    @property
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=3)