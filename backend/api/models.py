from django.db import models
from django.contrib.auth.models import User

# defined normally using Django models
class ChatMessage(models.Model): # chat storage model via Postgres
    session_id = models.CharField(max_length=100)
    user_query = models.TextField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# model for tracking what's in the db
class Document(models.Model):
    title = models.CharField(max_length=255)
    source_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# How to tell a developer from user
class UserProfile(models.Model):
    DEVELOPER = 'developer'
    END_USER = 'end_user'
    ROLE_CHOICES = [(DEVELOPER, 'Developer'), (END_USER, 'End User')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=END_USER)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


