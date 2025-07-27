from django.db import models
from django.conf import settings
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class Follow(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'follower'], name='unique_author_follower')
        ]

    def __str__(self):
        return f'{self.follower} follow {self.author}'


class Subscribe(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscribers')
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(choices=[
        (1, 'a month'),
        (3, 'three months'),
        (6, 'six months'),
        (12, 'a year'),
    ])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'subscriber'], name='unique_author_subscriber')
        ]

    def __str__(self):
        return f'{self.subscriber} subscribed {self.author}'
    
    @property
    def expired_at(self):
        return self.updated_at + relativedelta(months=self.duration)
    
    @property
    def is_active(self):
        return timezone.now() < self.expired_at