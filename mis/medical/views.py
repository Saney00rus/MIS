from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Doctor, DoctorSchedule, AppointmentSlot, Appointment
from .forms import PatientForm, PatientSearchForm, DoctorScheduleForm, DateSelectionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from django.db.models import Min
import dateparser


def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})


def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'patient_detail.html', {'patient': patient})


def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = PatientForm(instance=patient)

    return render(request, 'edit_patient.html', {'form': form})


def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'delete_patient.html', {'patient': patient})


@login_required(login_url='/doctor-login')
def doctor_dashboard(request, date=None):
    if date:
        try:
            selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = datetime.today().date()
    else:
        selected_date = datetime.today().date()

    # Получаем предыдущий и следующий день
    previous_date = (selected_date - timedelta(days=1)).strftime('%Y-%m-%d')
    next_date = (selected_date + timedelta(days=1)).strftime('%Y-%m-%d')

    today_date = selected_date.strftime('%d.%m.%Y')

    doctor = request.user.doctor
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.filter(doctor_id=doctor, date=selected_date)

    return render(request, 'doctor_dashboard.html',
                  {'doctor': doctor, 'doctors': doctors, 'appointments': appointments, 'today_date': today_date,
                   'previous_date': previous_date, 'next_date': next_date})


def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})


def doctor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('doctor_dashboard')
        else:
            error_message = 'Неправильное имя пользователя или пароль.'
    else:
        error_message = None

    return render(request, 'doctor_login.html', {'error_message': error_message})


def doctor_logout(request):
    logout(request)
    return redirect('doctor_login')


def search_patient(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        patients = Patient.objects.filter(full_name__icontains=search_query)
    else:
        patients = Patient.objects.all()
    return render(request, 'search_patient.html', {'patients': patients})


def patient_profile(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    doctors = Doctor.objects.all()
    return render(request, 'patient_profile.html', {'patient': patient, 'doctors': doctors})


def doctor_schedule(request, patient_id, doctor_id):
    patient = get_object_or_404(Patient, id=patient_id)
    doctor = get_object_or_404(Doctor, id=doctor_id)
    appointments = Appointment.objects.filter(doctor_id=doctor)
    time_slots = []

    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['date']
            appointments1 = appointments.filter(date=selected_date)
            for appointment in appointments1:
                if appointment.patient_id_id is not None:
                    is_available = False
                else:
                    is_available = True
                time_slots.append({
                    'time': appointment.time,
                    'is_available': is_available
                })
        else:
            selected_date = None
            time_slots = []
    else:
        form = DateSelectionForm()
        selected_date = None
        time_slots = []
    available_dates = list(appointments.values_list('date', flat=True).distinct())
    available_appointments = []

    for date in available_dates:
        available_appointments.append({
            'date': date.strftime('%Y-%m-%d'),
            'time_slots': time_slots
        })

    return render(request, 'doctor_schedule.html', {
        'patient': patient,
        'doctor': doctor,
        'available_appointments': available_appointments,
        'selected_date': selected_date,
        'time_slots': time_slots,
        'form': form,
    })


def confirm_appointment(request, patient_id, doctor_id):
    patient = get_object_or_404(Patient, id=patient_id)
    doctor = get_object_or_404(Doctor, id=doctor_id)
    selected_date = request.GET.get('date')
    selected_time = request.GET.get('time')

    def convert_date_format(date_string):
        # Используем dateparser для разбора даты
        parsed_date = dateparser.parse(date_string, languages=['ru'])

        # Если парсинг прошел успешно, то преобразуем дату в нужный формат
        if parsed_date:
            formatted_date = parsed_date.strftime('%Y-%m-%d')
            return formatted_date
        else:
            return None

    def extract_time(datetime_string):
        # Используем dateparser для разбора даты и времени
        parsed_datetime = dateparser.parse(datetime_string, languages=['ru'], settings={'TIMEZONE': 'UTC'})

        # Если парсинг прошел успешно, то извлекаем время
        if parsed_datetime:
            formatted_time = parsed_datetime.strftime('%H:%M')
            return formatted_time
        else:
            return None

    formatted_date = convert_date_format(selected_date)
    time_only = extract_time(selected_time)

    if request.method == 'POST':
        appointment = Appointment.objects.filter(date=formatted_date, time=time_only, doctor_id=doctor).first()
        if appointment:
            appointment.patient_id = patient
            appointment.save()
            return redirect('doctor_dashboard')

    return render(request, 'confirm_appointment.html', {
        'patient': patient,
        'doctor': doctor,
        'selected_date': selected_date,
        'selected_time': time_only,
    })


def doctor_schedule_settings(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        form = DoctorScheduleForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            # Создание записей в AppointmentSlot
            create_appointments(doctor)
            return redirect('doctor_dashboard')
    else:
        form = DoctorScheduleForm(instance=doctor)

    return render(request, 'doctor_schedule_settings.html', {'doctor': doctor, 'form': form})


def create_appointments(doctor):
    appointment_duration = doctor.appointment_duration
    delta = timedelta(minutes=appointment_duration)
    current_date = date.today()  # Используйте текущую дату или другую нужную вам начальную дату
    end_date = date.today() + timedelta(
        days=7)  # Используйте нужное количество дней или другую нужную вам конечную дату

    while current_date <= end_date:
        start_time = doctor.start_time
        end_time = doctor.end_time

        start_datetime = datetime.combine(current_date, start_time)
        end_datetime = datetime.combine(current_date, end_time)

        while start_datetime <= end_datetime - delta:
            appointment = Appointment(doctor_id=doctor, date=current_date, time=(start_datetime + delta).time(),
                                      appointment_duration=appointment_duration)
            appointment.save()
            start_datetime += delta

        current_date += timedelta(days=1)
