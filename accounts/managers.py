from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, phone, email, username, password=None):
        if not phone:
            raise ValueError('Users must have a phone number')
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        
        user = self.model(
            phone=phone,
            email=self.normalize_email(email),
            username=username
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, email, username, password=None):
        user = self.create_user(phone, email, username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user