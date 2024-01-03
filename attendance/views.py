from django.shortcuts import render,redirect
from home.models import Group, Attendance, Student, Teacher
from datetime import datetime
from datetime import timedelta
from django.db.models import Count, Q, F
from django.db.models import Sum

# Create your views here.



def home(request):
    if request.method == 'POST':
        group_id = request.POST.get('group')
        date = request.POST.get('date')
        group = Group.objects.get(id=group_id)
        students = group.students.all()
        for student in students:
            present = request.POST.get(f'present-{student.id}')
            attendance = Attendance(student=student, date=date, present=present)
            attendance.save()
        return redirect('attendance')
    else:
        groups = Group.objects.all()
        return render(request, 'attendance/home.html', {'groups': groups})


def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d').date()
        return True
    except ValueError:
        return False

def attendanceList(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date and is_valid_date(start_date) and is_valid_date(end_date):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

    students = Student.objects.prefetch_related('attendance_set').all().annotate(
        attended_days=Count('attendance', filter=Q(attendance__date__range=(start_date, end_date)), distinct=True)
    )

    data = []
    for student in students:
        attended_courses = {}
        for attendance in student.attendance_set.all():
            if attendance.date >= start_date and attendance.date <= end_date:
                course_name = attendance.course.name
                if course_name not in attended_courses:
                    attended_courses[course_name] = 0
                attended_courses[course_name] += 1
        data.append({'student': student, 'attended_courses': attended_courses})

    return render(request, 'attendance/attendance.html', {'students': data})

