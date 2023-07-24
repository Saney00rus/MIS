from django.db import models
from django.contrib.auth.models import User
from datetime import time


class Patient(models.Model):
    # Идентификационные данные
    full_name = models.CharField(verbose_name='ФИО', max_length=100)
    gender = models.CharField(verbose_name='Пол', max_length=10, choices=[('M', 'Мужской'), ('F', 'Женский')])
    birth_date = models.DateField(verbose_name='Дата рождения')
    insurance_number = models.CharField(verbose_name='Номер полиса', max_length=20)
    snils_number = models.CharField(verbose_name='Номер СНИЛС', max_length=20)
    military_rank = models.CharField(verbose_name='Воинское звание', max_length=50, blank=True, null=True)
    address = models.CharField(verbose_name='Адрес проживания', max_length=100)
    contact_number = models.CharField(verbose_name='Контактный номер', max_length=20)
    email = models.EmailField(verbose_name='Эл. почта', max_length=100)

    # Медицинская история
    medical_history = models.TextField(verbose_name='Анамнез заболеваний')
    chronic_conditions = models.TextField(verbose_name='Хронические заболевания')
    surgeries = models.TextField(verbose_name='История операций и процедур')
    allergies = models.TextField(verbose_name='Аллергические реакции и непереносимость лекарств')
    medical_tests = models.TextField(verbose_name='Результаты медицинских обследований')
    prescriptions = models.TextField(verbose_name='Рецепты и назначения лекарств')

    def __str__(self):
        return self.full_name


class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateField(verbose_name='Дата посещения')
    doctor = models.ForeignKey('medical.Doctor', on_delete=models.CASCADE)
    diagnosis = models.TextField(verbose_name='Диагноз')
    treatment_plan = models.TextField(verbose_name='План лечения и рекомендации')


class Vaccination(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vaccinations')
    vaccine = models.CharField(verbose_name='Прививка', max_length=100)
    vaccination_date = models.DateField(verbose_name='Дата вакцинации')


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name = models.CharField(verbose_name='Фамилия', max_length=100)
    first_name = models.CharField(verbose_name='Имя', max_length=100)
    middle_name = models.CharField(verbose_name='Отчество', max_length=50)
    specialization = models.CharField(verbose_name='Должность', max_length=100)
    contact_number = models.CharField(verbose_name='Телефон', max_length=20)
    start_time = models.TimeField(verbose_name='Время начала приема')
    end_time = models.TimeField(verbose_name='Время окончания приема')
    appointment_duration = models.PositiveIntegerField(verbose_name='Длительность приема в минутах')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Appointment(models.Model):
    date = models.DateField(verbose_name='Дата приема')
    time = models.TimeField(verbose_name='Время приема')
    appointment_duration = models.PositiveIntegerField(verbose_name='Длительность приема в минутах')
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='ID врача')
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True, verbose_name='ID пациента')

    def __str__(self):
        return f'{self.date} {self.time} - {self.doctor_id}'

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Записи на прием'


class AppointmentSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата приема')
    start_time = models.TimeField(verbose_name='Время начала приема')
    end_time = models.TimeField(verbose_name='Время окончания приема')

    def __str__(self):
        return f'{self.doctor} - {self.date} {self.start_time}-{self.end_time}'


class DoctorSchedule(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    start_time = models.TimeField(default=time(8, 0))
    end_time = models.TimeField(default=time(16, 30))
    appointment_duration = models.PositiveIntegerField(default=15)
