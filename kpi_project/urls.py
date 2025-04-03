from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kpi_app.urls')),  # Root path goes to kpi_app.urls
    path('login/', auth_views.LoginView.as_view(template_name='kpi_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]