from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Report

def report_list(request):
    """View to list all reports or search based on a query."""
    query = request.GET.get("search", "")
    if query:
        reports = Report.search_reports(query)
    else:
        reports = []  # Default: Show nothing until a search is made

    return render(request, "report_list.html", {"reports": reports, "search_query": query})

def create_report(request):
    """View to handle creating a new report."""
    if request.method == "POST":
        report_type = request.POST.get("report_type")
        value = request.POST.get("value")
        description = request.POST.get("description")

        if report_type and value and description:
            Report.create_report(report_type, value, description)
            return redirect("report_list")

    return render(request, "create_report.html")

def update_report(request, report_id):
    """View to handle updating an existing report."""
    if request.method == "POST":
        report_type = request.POST.get("report_type")
        value = request.POST.get("value")
        description = request.POST.get("description")

        if report_type and value and description:
            Report.update_report(report_id, report_type, value, description)
            return redirect("report_list")

    return render(request, "update_report.html", {"report_id": report_id})

def delete_report(request, report_id):
    """View to handle deleting a report."""
    if request.method == "POST":
        Report.delete_report(report_id)
        return JsonResponse({"success": True})

    return render(request, "delete_report.html", {"report_id": report_id})
