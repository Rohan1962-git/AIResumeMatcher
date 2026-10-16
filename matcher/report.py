
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import ResumeAnalysis


@login_required(login_url="login")
def download_report(request, analysis_id):
    analysis = get_object_or_404(
        ResumeAnalysis,
        id=analysis_id,
        user=request.user
    )

    report = f"""
AI RESUME MATCHER - ANALYSIS REPORT
===================================

Resume Name: {analysis.resume_name}
Match Score: {analysis.match_score}%
Analysis Date: {analysis.created_at.strftime("%d %B %Y, %I:%M %p")}

MATCHED SKILLS
--------------
{analysis.matched_skills or "None"}

MISSING SKILLS
--------------
{analysis.missing_skills or "None"}

JOB DESCRIPTION
---------------
{analysis.job_description}
"""

    response = HttpResponse(
        report,
        content_type="text/plain; charset=utf-8"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="resume_report_{analysis.id}.txt"'
    )

    return response