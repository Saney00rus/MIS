from django.contrib.auth.models import Group


def is_medregistrator(request):
    return {
        'is_medregistrator': request.user.groups.filter(name='Медрегистратор').exists()
    }


def is_doctor(request):
    return {
        'is_doctor': request.user.groups.filter(name='Doctors').exists()
    }
