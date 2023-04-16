from todoapp.models import *

def get_status(request):
    return {'statuses': TaskStatus.objects.all()}

def get_type(request):
    return {'types': TaskType.objects.all()}
