from django import forms
from .models import Patient, Doctor
from datetime import date


class PatientForm(forms.ModelForm):
    birth_date = forms.DateField(input_formats=['%d.%m.%Y'])

    class Meta:
        model = Patient
        fields = '__all__'


class PatientSearchForm(forms.Form):
    last_name = forms.CharField(label='Фамилия', max_length=50)


class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['start_time', 'end_time', 'appointment_duration']


class DateSelectionForm(forms.Form):
    date = forms.DateField(label='Выберите дату',
                           widget=forms.DateInput(attrs={'type': 'date', 'min': str(date.today())}))
