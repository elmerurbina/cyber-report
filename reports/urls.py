from django.urls import path
from . import views

urlpatterns = [
    path("", views.report_list, name="report_list"),
    path("create/", views.create_report, name="create_report"),
    path("update/<int:report_id>/", views.update_report, name="update_report"),
    path("delete/<int:report_id>/", views.delete_report, name="delete_report"),
]
