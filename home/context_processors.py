from home.models import Admin, Boshliq, Teacher
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
def role(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        if Admin.objects.filter(user=user).exists():
            context['role'] = 'admin'
        elif Teacher.objects.filter(user=user).exists():
            context['role'] = 'teacher'
        elif Boshliq.objects.filter(user=user).exists():
            context['role'] = 'boshliq'
    return context


