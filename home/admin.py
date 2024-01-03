from django.contrib import admin
from .models import Course, Group, Student, Payment, Teacher, Admin,Attendance,TeacherAttendance,Applicant, Boshliq, AlertMessages
# Register your models here.

admin.site.register(Course)
class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('students',)

admin.site.register(Group, GroupAdmin)
admin.site.register(Student)
admin.site.register(Payment)
admin.site.register(Teacher)
admin.site.register(Boshliq)
admin.site.register(Admin)
admin.site.register(Attendance)
admin.site.register(TeacherAttendance)
admin.site.register(Applicant)
admin.site.register(AlertMessages)
