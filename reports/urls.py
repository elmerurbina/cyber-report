from django.urls import path
from . import views
from .views import report_list, create_report

urlpatterns = [
    path("", views.report_list, name="report_list"),

    path('', report_list, name='report_list'),  # Show reports
    path('create/', create_report, name='create_report'),

]
