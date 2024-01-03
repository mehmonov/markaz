
from django.shortcuts import render,redirect,get_object_or_404
from home.models import Attendance, Course,Admin, Applicant, Payment,Student, Group
from .forms import ApplicantForm, GroupForm,StudentGroupChangeForm,GroupEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.cache import cache
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from datetime import date
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import HttpResponse


# Create your views here.

def adminHome(request):
    return render(request,template_name='admin/home.html')

def newApplicant(request):
    if not request.user.is_authenticated:
        print('balki shu admin login qilmagan')
    if request.method == 'POST':
        form = ApplicantForm(request.POST)
        if form.is_valid():
            applicant_data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'birth_place': form.cleaned_data['birth_place'],
                'preferred_time': form.cleaned_data['preferred_time'],
                'course': form.cleaned_data['course'],
                'preferred_days_of_week': form.cleaned_data['preferred_days_of_week'],
                'phone_number': form.cleaned_data['phone_number'],
                'phone_number2': form.cleaned_data['phone_number2']
            }
            applicant, created = Applicant.objects.get_or_create(**applicant_data)
            if not created:
                return HttpResponse('imkoni yoq. oldin royhatdan otgan')
            else:
                try:
                    admin_user = Admin.objects.get(user=request.user)
                    applicant.registered_by = admin_user
                    applicant.save()
                    return redirect('adminHome')
                except Admin.DoesNotExist:
                    return HttpResponse('admin emassiz') 
    else:
        form = ApplicantForm()
        return render(request, 'admin/applicant.html', {'form': form})

def applicantList(request):
  
    course = Course.objects.all()
    applicants = Applicant.objects.filter(student__isnull=True)
    context = {'applicants': applicants,'course':course}
    return render(request,template_name='admin/applicant_list.html',context=context)

def filter_applicants(request):
    course = request.GET.get('course')
    preferred_time = request.GET.get('preferred_time')
    search = request.GET.get('search')

    cache_key = f'applicants-{course}-{preferred_time}-{search}'
    data = cache.get(cache_key)

    if data is None:
        applicants = Applicant.objects.filter(student__isnull=True).select_related('course')

        if course:
            applicants = applicants.filter(course__id=course)
        if preferred_time:
            applicants = applicants.filter(preferred_time=preferred_time)
        if search:
            applicants = applicants.filter(first_name__icontains=search) | \
                         applicants.filter(last_name__icontains=search)

        data = list(applicants.values('first_name', 'course__name', 'preferred_time', 'phone_number'))
        cache.set(cache_key, data, 300)

    return JsonResponse(data, safe=False)
def create_student_from_applicant(request, applicant):
    try:
        # Get the Admin object using get_object_or_404
        admin = get_object_or_404(Admin, user=request.user)
        # Create or update the Student instance using data from the Applicant instance
        student, created = Student.objects.update_or_create(
            applicant=applicant,
            defaults={
                'first_name': applicant.first_name,
                'last_name': applicant.last_name,
                'birth_place': applicant.birth_place,
                'phone_number': applicant.phone_number,
                'phone_number2': applicant.phone_number2,
                'email': applicant.email,
                
                'registered_by': admin
            }
        )
        # Set the course field using the set() method
        student.courses = student.course.all()

        # Set the student field on the Applicant instance to link the two instances
        applicant.student = student
        applicant.save()
        # Add a success message
        messages.success(request, 'Student successfully created.')
    except Exception as e:
        # Add an error message
        messages.error(request, f'An error occurred: {e}')

def transfer_applicant(request, application_id):
    try:
        # Get the Applicant instance with the given application_id
        applicant = get_object_or_404(Applicant, pk=application_id)
        # Call the create_student_from_applicant function to create a new Student instance
        create_student_from_applicant(request, applicant)
    except Exception as e:
        # Add an error message
        messages.error(request, f'An error occurred: {e}')
    # Redirect to a success page or display a success message
    return redirect('adminHome')

def studentList(request):
    students = Student.objects.all()
    payments = Payment.objects.all()
    allCourse = Course.objects.all()

    # Filter by course
    course = request.GET.get('course')
    if course:
        students = students.filter(course__name=course)
    
    # Filter by payment status
    payment_status = request.GET.get('payment_status')
    if payment_status:
        if payment_status == 'paid':
            students = students.filter(payment__isnull=False)
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
    return render(request, template_name='admin/student_list.html', context=context)

def createGroup(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            students = form.cleaned_data['students']
            # Check if more than 15 students are selected
            students = form.cleaned_data['students']
            if len(students) > 15:
                # More than 15 students are selected, so raise a validation error
                form.add_error('students', 'No more than 15 students can be selected')
                return render(request, template_name='admin/create_group.html', context={'form': form})

            for student in students:
                student.group.set([group])
                student.start_day = date.today()
                student.course.add(group.course)
                student.save()
            return redirect('adminHome')
        else:
            context = {
                'form': form,
            }
            return render(request, template_name='admin/create_group.html', context=context)

    else:
        students = Student.objects.filter(group__isnull=True)
        form = GroupForm()
        context = {
            'form':form,
        }
        return render(request, template_name='admin/create_group.html',context=context)

def student_group_change(request, student_id):
    # Get the student with the given ID
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        # Create a StudentGroupChangeForm instance with the submitted data
        form = StudentGroupChangeForm(request.POST, instance=student)
        if form.is_valid():
            # Update the student's group information
            form.save()
            
            # Redirect to a success page
            return redirect('studentList')
    else:
        # Create a StudentGroupChangeForm instance with the initial data from the student
        form = StudentGroupChangeForm(instance=student)
    
    # Render the form template
    context = {
        'form': form,
        'student': student,
    }
    return render(request, 'admin/student_group_change.html', context)

def add_students_to_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'GET':
        students = Student.objects.exclude(groups__in=[group])
        return render(request, 'group/add_students.html', {'group': group, 'students': students})
    elif request.method == 'POST':
        student_ids = request.POST.getlist('students')
        students = Student.objects.filter(id__in=student_ids)
        group.students.add(*students)
        return redirect('group_detail', group_id=group.id)

def groupList(request):
    groups = Group.objects.all()
    group_data = []
    for group in groups:
        student_count = group.students.count()
        group_data.append({'group': group, 'student_count': student_count})
    context = {'groups': group_data}
    
    return render(request, template_name='group/home.html',context=context)

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    students = group.students.all()
    
    attendance_data = {}
    for student in students:
        attendance_count = Attendance.objects.filter(student=student, group=group).count()
        attendance_data[student.id] = attendance_count
        
       
    context = {'group': group, 'students': students, 'attendance_data': attendance_data}
    
    return render(request, 'group/group_detail.html', context)

def groupEdit(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = GroupEditForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm(instance=group)
    context = {'form': form}
    return render(request, 'group/groupEdit.html', context)

def leave_group(request, group_id, student_id):
    try:
        # Get the student object using the student_id
        student = Student.objects.get(id=student_id)
        # Get the group object using the group_id
        group = Group.objects.get(id=group_id)
        # Remove the group from the student's groups
        student.groups.remove(group)
        # Add a success message
        messages.success(request, 'student chiqarib yuborildi')
    except Exception as e:
        # Add an error message
        messages.error(request, f'An error occurred: {e}')
    # Redirect to the group detail page
    return redirect('group_detail', group_id=group_id)

def group_payments(request):
    groups = Group.objects.all()
    payments = []
    for group in groups:
        students = group.students.filter(status='uncompleted')
        for student in students:
            student_payments = Payment.objects.filter(student=student, course=group.course)
            payments.append({
                'group': group,
                'student': student,
                'payments': student_payments
            })
                        
    return render(request, 'group/group_payments.html', {'payments': payments})

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    payments = Payment.objects.filter(student=student)
    return render(request, 'student/home.html', {'student': student, 'payments': payments})   