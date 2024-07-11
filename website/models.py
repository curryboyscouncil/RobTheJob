from datetime import datetime, date
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Resume(models.Model):
    # def validate_resume_fields(fields):
    #     if not 0 < fields <= 5:
    #         raise ValidationError(
    #             f'Rating needs to be in rang (1,5) found : {productivity_rating}')

    resume_text = models.TextField(max_length=15_000)
    cv = models.TextField(max_length=15_000)
    jd = models.TextField(max_length=15_000)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Resume ID: {self.id}'