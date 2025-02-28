from django.shortcuts import render, redirect
from .models import Report

def report_list(request):
    """View to list all reports or search based on a query."""
    query = request.GET.get("search", "")
    reports = Report.objects.all()

    if query:
        reports = reports.filter(value__icontains=query)

    return render(request, "home.html", {"reports": reports, "search_query": query})

def create_report(request):
    """View to handle creating a new report."""
    if request.method == "POST":
        report_type = request.POST.get("report_type")
        value = request.POST.get("value")
        description = request.POST.get("description")

        if report_type and value and description:
            Report.objects.create(report_type=report_type, value=value, description=description)
            return redirect("report_list")

    return render(request, "report.html")  # Show form for creating a report
