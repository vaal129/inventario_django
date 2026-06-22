from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/', views.passenger_dashboard, name='passenger_dashboard'),
    path('toggle-user/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('api/reports/', views.api_reports, name='api_reports'),
    path('api/notifications/', views.api_notifications, name='api_notifications'),
    path('submit_report/', views.submit_report, name='submit_report'),
    path('update_report_status/<int:report_id>/', views.update_report_status, name='update_report_status'),
    path('delete_report/<int:report_id>/', views.delete_report, name='delete_report'),
    path('create_notification/', views.create_notification, name='create_notification'),
]