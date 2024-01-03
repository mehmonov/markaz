from django.shortcuts import render, redirect
from django.utils import timezone
from home.models import Applicant, Attendance, Group, Payment, Student, Admin, Course, Teacher
from django.db.models import Sum
from django.http import JsonResponse

from datetime import datetime, timedelta
from django.db.models import Count, Sum
from django.db.models import Count, F, Q
# Create your views here.
teachers = Teacher.objects.all()

def home(request):
    today = timezone.now().date()
    payments = Payment.unconfirmed_objects.filter(date__date=today)
    total_payments = Payment.unconfirmed_objects.filter(date__date=today)
    
    total_amount = payments.aggregate(Sum('amount'))['amount__sum']
    today_applicants = Applicant.objects.filter(registered_time__date=today).count()
    today_students = Applicant.objects.filter(registered_time__date=today, student__isnull=False).count()

    today_attendance = Attendance.objects.filter(date=today, should_attend=True).values('student').distinct().count()

    today_day = today.strftime('%A')
    today_groups = Group.objects.filter(day_of_week__contains=[today_day]).count()

    context = {
        'total_payments': total_payments,
        'total_amount': total_amount,
        'today_applicants':today_applicants,
        'today_students': today_students,
        'today_attendance': today_attendance,
        'today_groups':today_groups
        
    }
    return render(request, template_name='boshliq/home.html', context=context)
def studentList(request):
    students = Student.objects.all()
    payments = Payment.confirmed_objects.all()
    allCourse = Course.objects.all()

    # Filter  bycourse
    course = request.GET.get('course')
    if course:
        students = students.filter(course__name=course)
    
    # Filter by payment status
    payment_status = request.GET.get('payment_status')
    if payment_status:
        if payment_status == 'paid':
            students = students.filter(payment__isnull=False).distinct()
        elif payment_status == 'not_paid':
            students = students.filter(payment__isnull=True)
    
    student_payments = []
    for student in students:
        student_payment = payments.filter(student=student)
        student_courses = student.course.all()
        student_payments.append({
            'student': student,
            'payments': student_payment,
            'courses': student_courses
        })
    context = {
        'students': student_payments,
        'allCourse': allCourse
    }
   
    return render(request, template_name='boshliq/student_list.html', context=context)

def all_incomes(request):
    payments = Payment.confirmed_objects.all()
    courses = Course.objects.all()
    # Filter by course
    course = request.GET.get('course')
    if course:
        payments = payments.filter(student__course__name=course)
    
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        payments = payments.filter(date__range=(start_date, end_date))
    else:
        # Show payments from the last 30 days
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
    
    
    context = {
        'payments': payments,
        'start_date': start_date,
        'end_date': end_date,
        'courses':courses
    }
    return render(request, template_name='boshliq/incomes.html', context=context)

def all_incomes_filter(request):
    # Get the filter values from the request
    course = request.GET.get('course')
    start_day = request.GET.get('start_day')
    end_day = request.GET.get('end_day')
    # Filter the payments based on the filter values
    payments = Payment.objects.all()
    if course:
        payments = payments.filter(course__id=course)
    if start_day:
        payments = payments.filter(date__gte=start_day)
    if end_day:
        payments = payments.filter(date__lte=end_day)

    # Convert the filtered payments into a format that can be serialized as JSON
    data = []
    for payment in payments:
        data.append({
            'first_name': payment.student.first_name,
            'course': [str(course) for course in payment.student.course.all()],
            'group': [str(group) for group in payment.student.group.all()],
            'last_payment': payment.date.strftime('%Y-%m-%d'),
            'payment_amount': str(payment.amount),
        })

    # Return a JSON response containing the filtered data
    return JsonResponse(data, safe=False)

def all_groups(request):
    teachers = Teacher.objects.all()
    # Calculate the number of students and the total amount of payments for each group
    groups = Group.objects.annotate(
        num_students=Count('student'),
        total_payments=Sum('student__payment__amount')
    )
    # Pass the groups data to the template context
    context = {
        'teachers':teachers,
        'groups': groups,
    }
    return render(request, 'boshliq/groups.html', context)
def get_groups(request):
    groups = Group.objects.all()
    if request.GET.get('last_month_created'):
        # Agar "oxirgi oy" tugmasi bosilgan bo'lsa
        last_month = datetime.now() - timedelta(days=30)
        groups = groups.filter(start_date__gte=last_month)
    if request.GET.get('min_payments'):
        # Agar "eng kam to'lov qilganlar" tugmasi bosilgan bo'lsa
        groups = groups.annotate(
            total_payments=Sum('payment__amount'),
            num_students=Count('students'),
            payment_percentage=F('total_payments') / F('num_students')
        ).order_by('payment_percentage')
    if not request.GET.get('active_and_unactive_group'):
        # Agar "aktive emas guruhlar" tugmasi bosilmagan bo'lsa
        groups = groups.filter(status='uncompleted')
    if request.GET.get('teacher'):
        # Agar o'qituvchi tanlangan bo'lsa
        teacher_id = int(request.GET.get('teacher'))
        groups = groups.filter(teacher__id=teacher_id)
    # Boshqa filterlar uchun shu usulda kodni yozishingiz mumkin
    data = []
    for group in groups:
        total_payments = group.payment_set.aggregate(Sum('amount'))['amount__sum']
        if total_payments is None:
            total_payments = 0
        data.append({
            'name': group.name,
            'num_students': group.students.count(),
            'total_payments': total_payments,
            'teacher': group.teacher.user.first_name,
            'start_date': group.start_date,
            'end_date': group.end_date,
        })
    return JsonResponse(data, safe=False)

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d').date()
        return True
    except ValueError:
        return False


def teacher_payments(request):
    teacher_id = request.GET.get('teacher_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
  
    if start_date and end_date and is_valid_date(start_date) and is_valid_date(end_date):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
    
    teachers = Teacher.objects.all()
    if teacher_id:
        teachers = teachers.filter(id=teacher_id)
    
    data = []
    for teacher in teachers:
        groups = Group.objects.filter(teacher=teacher)
        payments = Payment.confirmed_objects.filter(group__in=groups, date__date__range=(start_date, end_date))
        total_students = payments.count()
        total_payment = payments.aggregate(Sum('amount'))['amount__sum']
        data.append({
            'teacher': teacher.user.first_name,
            'total_students': total_students,
            'total_payment': total_payment,
        })
       
    return data

def salary(request):
    
    data = teacher_payments(request)
    
   
    return render(request, 'boshliq/salary.html',{'data':data,'teachers':teachers})

def salary_filter(request):
    data = teacher_payments(request)
    
    return JsonResponse(data, safe=False)


def today_check_payments(request):
    today = timezone.now().date()
    payments = Payment.unconfirmed_objects.filter(date__date=today)
    total_payments = payments.aggregate(Sum('amount'))['amount__sum']

    context = {
        'payments': payments,
        'total_payments':total_payments
    }
    return render(request, 'boshliq/today_check_payments.html',context)

def confirm_payments(request):
    payment_ids = request.POST.getlist('payment_ids')
    payments = Payment.unconfirmed_objects.filter(id__in=payment_ids)
    payments.update(is_confirmed=True)
    return redirect('salary')