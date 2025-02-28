from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import HttpResponse

# Simple home page view
def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reports/', include('reports.urls')),  # Include reports app URLs
    path('', home, name='home'),  # Add this line to handle the root path
]
