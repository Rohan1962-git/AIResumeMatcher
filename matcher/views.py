from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .pdf_report import download_pdf_report
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from .analyzer import (
    calculate_match,
    get_skill_suggestions,
    check_resume_quality,
    extract_resume_text,
    check_ats_resume,
)
from .recommendations import recommend_jobs
from .forms import ResumeAnalysisForm, JobApplicationForm
from .models import ResumeAnalysis, JobApplication




def home(request):
    result = None
    saved_analysis = None

    form = ResumeAnalysisForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST" and form.is_valid():
        uploaded_file = form.cleaned_data["resume"]
        job_description = form.cleaned_data["job_description"]

        try:
            if uploaded_file.size > 5 * 1024 * 1024:
                raise ValueError("Please upload a file smaller than 5 MB.")

            if not uploaded_file.name.lower().endswith((".pdf", ".docx")):
                raise ValueError("Only PDF and DOCX files are supported.")

            resume_text = extract_resume_text(uploaded_file)
            result = calculate_match(resume_text, job_description)
            result["ats_report"] = check_ats_resume(
    resume_text,
    job_description
)
            result["resume_quality"] = check_resume_quality(resume_text)
            result["suggestions"] = get_skill_suggestions(
               result["missing_skills"]
            )
            result["job_recommendations"] = recommend_jobs(resume_text)
            

            print("ANALYSIS COMPLETED - SAVING TO DATABASE")

            saved_analysis = ResumeAnalysis.objects.create(
                user=request.user if request.user.is_authenticated else None,
                resume_name=uploaded_file.name,
                job_description=job_description,
                match_score=result["score"],
                matched_skills=", ".join(result["matched_skills"]),
                missing_skills=", ".join(result["missing_skills"])
            )

            print("ANALYSIS SAVED SUCCESSFULLY:", saved_analysis.id)

        except Exception as error:
            print("RESUME ANALYSIS ERROR:", repr(error))
            form.add_error("resume", str(error))

    return render(
    request,
    "matcher/home.html",
    {
        "form": form,
        "result": result,
        "analysis": saved_analysis,
    }
)

@login_required(login_url="login")
def history(request):
    analyses = ResumeAnalysis.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "matcher/history.html",
        {"analyses": analyses}
    )

@login_required(login_url="login")
def compare_jobs(request):
    comparison = None
    error = None

    if request.method == "POST":
        uploaded_file = request.FILES.get("resume")
        job_description_1 = request.POST.get("job_description_1", "").strip()
        job_description_2 = request.POST.get("job_description_2", "").strip()

        if not uploaded_file:
            error = "Please upload your resume."
        elif not uploaded_file.name.lower().endswith((".pdf", ".docx")):
            error = "Only PDF and DOCX files are supported."
        elif uploaded_file.size > 5 * 1024 * 1024:
            error = "Please upload a file smaller than 5 MB."
        elif not job_description_1 or not job_description_2:
            error = "Please enter both job descriptions."
        else:
            try:
                resume_text = extract_resume_text(uploaded_file)

                result_1 = calculate_match(resume_text, job_description_1)
                result_2 = calculate_match(resume_text, job_description_2)

                comparison = {
                    "score_1": result_1["score"],
                    "score_2": result_2["score"],
                    "matched_1": result_1["matched_skills"],
                    "matched_2": result_2["matched_skills"],
                    "missing_1": result_1["missing_skills"],
                    "missing_2": result_2["missing_skills"],
                }
            except Exception as exc:
                error = f"Could not compare jobs: {exc}"

    return render(
        request,
        "matcher/compare_jobs.html",
        {"comparison": comparison, "error": error},
    )


@login_required(login_url="login")

@login_required(login_url="login")
def dashboard(request):
    applications = JobApplication.objects.filter(
        user=request.user
    )

    context = {
        "total_applications": applications.count(),
        "saved_count": applications.filter(status="saved").count(),
        "applied_count": applications.filter(status="applied").count(),
        "interview_count": applications.filter(status="interview").count(),
        "rejected_count": applications.filter(status="rejected").count(),
        "offer_count": applications.filter(status="offer").count(),
        "recent_applications": applications.order_by("-created_at")[:5],
    }

    return render(
        request,
        "matcher/dashboard.html",
        context,
    )

    

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "matcher/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "matcher/login.html", {"form": form})

def user_logout(request):
    if request.method == "POST":
        logout(request)

    return redirect("home")


@login_required(login_url="login")
def download_report(request, analysis_id):
    analysis = get_object_or_404(
        ResumeAnalysis,
        id=analysis_id,
        user=request.user,
    )

    report_text = f"""
AI RESUME MATCHER
Resume Analysis Report

Resume: {analysis.resume_name}
Analysis Date: {analysis.created_at.strftime('%d %B %Y, %I:%M %p')}
Overall Match Score: {analysis.match_score}%

Matching Skills:
{analysis.matched_skills or "No matching skills found."}

Skills to Develop:
{analysis.missing_skills or "No missing skills recorded."}
"""

    response = HttpResponse(
        report_text,
        content_type="text/plain; charset=utf-8",
    )
    response["Content-Disposition"] = (
        'attachment; filename="resume_analysis_report.txt"'
    )

    return response


@login_required(login_url="login")
def job_applications(request):
    if request.method == "POST":
        form = JobApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect("job_applications")
    else:
        form = JobApplicationForm()

    applications = JobApplication.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "matcher/job_applications.html",
        {
            "form": form,
            "applications": applications,
        },
    )


@login_required(login_url="login")
def edit_job_application(request, application_id):
    application = get_object_or_404(
        JobApplication,
        id=application_id,
        user=request.user
    )

    if request.method == "POST":
        form = JobApplicationForm(
            request.POST,
            instance=application
        )
        if form.is_valid():
            form.save()
            return redirect("job_applications")
    else:
        form = JobApplicationForm(instance=application)

    return render(
        request,
        "matcher/edit_job_application.html",
        {
            "form": form,
            "application": application,
        },
    )


@login_required(login_url="login")
def delete_job_application(request, application_id):
    application = get_object_or_404(
        JobApplication,
        id=application_id,
        user=request.user
    )

    if request.method == "POST":
        application.delete()
        return redirect("job_applications")

    return render(
        request,
        "matcher/delete_job_application.html",
        {"application": application},
    )

