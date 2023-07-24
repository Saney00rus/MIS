from django.contrib import admin
from .models import Patient
from .models import Doctor

admin.site.register(Doctor)
# @admin.register(Patient)
# class PatientAdmin(admin.ModelAdmin):
#     list_display = ('last_name', 'first_name', 'middle_name', 'date_of_birth', 'gender', 'passport')
