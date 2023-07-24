from django.contrib import admin
from django.urls import path
from medical import views

urlpatterns = [
    path('', views.doctor_dashboard, name='doctor_dashboard'),
    path('admin/', admin.site.urls),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('patients/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('doctor-login/', views.doctor_login, name='doctor_login'),
    path('doctor-logout/', views.doctor_logout, name='doctor_logout'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor_dashboard/<str:date>/', views.doctor_dashboard, name='doctor_dashboard_with_date'),
    path('search-patient/', views.search_patient, name='search_patient'),
    path('patient-profile/<int:patient_id>/', views.patient_profile, name='patient_profile'),
    # path('choose-doctor/<int:patient_id>/', views.choose_doctor, name='choose_doctor'),
    path('confirm-appointment/<int:patient_id>/<int:doctor_id>', views.confirm_appointment, name='confirm_appointment'),
    path('doctor-schedule/<int:patient_id>/<int:doctor_id>/', views.doctor_schedule, name='doctor_schedule'),
    path('doctor/<int:doctor_id>/schedule-settings/', views.doctor_schedule_settings, name='doctor_schedule_settings'),
]
