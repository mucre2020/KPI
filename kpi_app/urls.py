from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('download/', views.download_summary, name='download_summary'),
    path('unit-details/', views.unit_details, name='unit_details'),  # New URL
]