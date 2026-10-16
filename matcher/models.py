
from django.db import models
from django.contrib.auth.models import User


class ResumeAnalysis(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    resume_name = models.CharField(max_length=255)
    job_description = models.TextField()
    match_score = models.PositiveIntegerField()
    matched_skills = models.TextField(blank=True)
    missing_skills = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("saved", "Saved"),
        ("applied", "Applied"),
        ("interview", "Interview"),
        ("rejected", "Rejected"),
        ("offer", "Offer Received"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    company_name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=150)
    job_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="saved"
    )
    notes = models.TextField(blank=True)
    applied_date = models.DateField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_title} - {self.company_name}"


   