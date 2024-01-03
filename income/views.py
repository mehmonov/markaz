from django.shortcuts import render,redirect
from home.models import Student, Course,Payment, Admin
from django.http import JsonResponse
from django.core.cache import cache
from .forms import PaymentForm

def home(request):
    return render(request, template_name='income/home.html')

def search(request):
    search_value = request.GET.get('search')
    # query Student model for matching data
    students = Student.objects.filter(first_name__icontains=search_value)
    student_data = list(students.values('first_name', 'group__name','id'))
    return JsonResponse(student_data, safe=False)

def paymentStudents(request, student_id):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        
        if form.is_valid():
            student = Student.objects.get(id=student_id)
            
            payment = form.save(commit=False)
            payment.student = student
            
            # Check if the current user is an admin
            if request.user.is_authenticated and isinstance(request.user, Admin):
                payment.admin = request.user
            
            # Save the Payment object to the database
            payment.save()
           
            return redirect('adminHome')
    else:
        form = PaymentForm()
    
    return render(request, template_name='income/incomeStudents.html', context={'form': form})
   