
from django import forms
from .models import ResumeAnalysis, JobApplication


class ResumeAnalysisForm(forms.Form):
    resume = forms.FileField(
        label="Upload Your Resume (PDF or DOCX or JPEG)"
    )

    job_description = forms.CharField(
        label="Paste Job Description",
        widget=forms.Textarea(attrs={
            "rows": 8,
            "placeholder": "Paste the job requirements here..."
        })
    )


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            "company_name",
            "job_title",
            "job_url",
            "status",
            "notes",
            "applied_date",
        ]
        widgets = {
            "applied_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "notes": forms.Textarea(
                attrs={"rows": 3}
            ),
        }
