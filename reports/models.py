from django.db import models, connection
from datetime import datetime

class Report(models.Model):
    REPORT_TYPES = [
        ('email', 'Email'),
        ('phone', 'Phone Number'),
        ('url', 'URL'),
        ('other', 'Other'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    value = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(null=True, blank=True)  # Optional, for future user tracking

    class Meta:
        managed = False  # We are using direct SQL procedures, not Django ORM
        db_table = "reports"

    @staticmethod
    def create_report(report_type, value, description, user_id=None):
        """Call the stored procedure to insert a new report."""
        with connection.cursor() as cursor:
            cursor.callproc("insert_report", [report_type, value, description, user_id])

    @staticmethod
    def update_report(report_id, report_type, value, description):
        """Call the stored procedure to update an existing report."""
        with connection.cursor() as cursor:
            cursor.callproc("update_report", [report_id, report_type, value, description])

    @staticmethod
    def delete_report(report_id):
        """Call the stored procedure to delete a report."""
        with connection.cursor() as cursor:
            cursor.callproc("delete_report", [report_id])

    @staticmethod
    def search_reports(query):
        """Call the search function to find reports based on email, phone, or URL."""
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM search_reports(%s)", [query])
            return cursor.fetchall()  # Returns a list of matching reports
