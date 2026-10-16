
from django.urls import path
from . import views
from .pdf_report import download_pdf_report

urlpatterns = [
    path("", views.home, name="home"),
    path("history/", views.history, name="history"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    path(
        "download-report/<int:analysis_id>/",
        views.download_report,
        name="download_report",
    ),
    path(
        "download-pdf-report/<int:analysis_id>/",
        download_pdf_report,
        name="download_pdf_report",
    ),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("compare-jobs/", views.compare_jobs, name="compare_jobs"),

    path(
        "job-applications/",
        views.job_applications,
        name="job_applications",
    ),
    path(
        "job-applications/<int:application_id>/edit/",
        views.edit_job_application,
        name="edit_job_application",
    ),
    path(
        "job-applications/<int:application_id>/delete/",
        views.delete_job_application,
        name="delete_job_application",
    ),
]
