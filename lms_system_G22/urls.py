from django import views
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lms/', include("lms.urls")),
    path(('accounts/'), include('django.contrib.auth.urls')),
    path('', lambda request: redirect('lms/', permanent=True)),  # Redirect root to /lms/
]



