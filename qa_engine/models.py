from django.conf import settings
from django.db import models

# Create your models here.

class DoubtEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question_text = models.TextField()
    full_prompt_sent = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    subject_category = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.subject_category or 'Uncategorized'} - {self.timestamp}"
