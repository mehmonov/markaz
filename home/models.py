from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.core.validators import RegexValidator
PREFERRED_DAYS_OF_WEEK_CHOICES = [
    ('Monday', 'Dushanba'),
    ('Tuesday', 'Seshanba'),
    ('Wednesday', 'Chorshanba'),
    ('Thursday', 'Payshanba'),
    ('Friday', 'Juma'),
    ('Saturday', 'shanba')
]
STATUS = [
    ('completed', 'tugagan'),
    ('uncompleted', 'tugatmagan'),
]
phone_regex = RegexValidator(
    regex=r'^9989\d{9}$',
    message="telefon raqam 9989 bilan boshlanishi kerak"
)


class ConfirmedPaymentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_confirmed=True)

class UnconfirmedPaymentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_confirmed=False)


class Boshliq(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    coupon = models.CharField(max_length=30, blank=True)
    teacher = models.ManyToManyField('Teacher')

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    date_of_birth = models.DateField()
    date_joined = models.DateField()
    status = models.CharField(
        choices=STATUS, default='uncompleted', verbose_name='status teacher')

    def __str__(self):
        return self.user.first_name


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(
        choices=STATUS, default='uncompleted', verbose_name='status admin')

    def __str__(self):
        return self.user.first_name


class Student(models.Model):
    applicant = models.OneToOneField(
        'Applicant', on_delete=models.SET_NULL, null=True, related_name='application_student', blank=True)
    group = models.ManyToManyField('Group', blank=True)
    first_name = models.CharField(
        max_length=30, verbose_name='Ism',)
    last_name = models.CharField(
        max_length=30, verbose_name='Familiya', blank=True, null=True
        )
    birth_place = models.CharField(
        max_length=100, blank=True, verbose_name='Tug\'lgan joy')
    course = models.ManyToManyField('Course', blank=True, verbose_name='Kurs')
    registered_by = models.ForeignKey(
        Admin, on_delete=models.SET_NULL, null=True, verbose_name='admin')
    phone_number = models.CharField(
        max_length=20, verbose_name='Raqam', default='Default phone')
    phone_number2 = models.CharField(
        max_length=20, blank=True, verbose_name='Raqam 2')
    email = models.EmailField(blank=True, null=True)
    start_day = models.DateField(null=True)
    status = models.CharField(
        choices=STATUS, default='uncompleted', verbose_name='status student')

    def __str__(self):
        return self.first_name


class Group(models.Model):
    DURATION_CHOISE = [
        ('1', '1 soat'),
        ('1.5', '1 soat 30 daqiqa'),
        ('2', '2 soat'),
    ]
    duration = models.CharField(
        choices=DURATION_CHOISE, default='1.5', verbose_name='dars davomiyligi')
    teacher = models.ForeignKey(
        'Teacher', on_delete=models.CASCADE, verbose_name='group teacher')
    name = models.CharField(max_length=100)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    students = models.ManyToManyField(Student, related_name='groups')
    time = models.TimeField()
    day_of_week = ArrayField(models.CharField(), verbose_name='Dars kunlari')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        choices=STATUS, default='uncompleted', verbose_name='status group')

    def __str__(self):
        return self.name


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('online', 'Online'),
    ]
    confirmed_objects = ConfirmedPaymentManager()
    unconfirmed_objects = UnconfirmedPaymentManager()

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHODS, default='cash')
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Set the value of the course field based on the selected group
        self.course = self.group.course
        super().save(*args, **kwargs)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, blank=True)
    should_attend = models.BooleanField(default=True)


class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField()
    recorded_by = models.ForeignKey(Admin, on_delete=models.CASCADE)


class Applicant(models.Model):
    TIME_CHOICES = [('morning', 'Abetdan oldin'), ('afternoon',
                                                   'Abetdan keyin'), ('anytime', 'Farqi yo\'q')]

    student = models.OneToOneField(
        Student, on_delete=models.SET_NULL, null=True, related_name='student', blank=True)
    first_name = models.CharField(max_length=30, verbose_name='Ism')
    last_name = models.CharField(max_length=30, verbose_name='Familiya')
    birth_place = models.CharField(
        max_length=100, blank=True, verbose_name='Tug\'lgan joy')
    preferred_time = models.CharField(
        max_length=10, choices=TIME_CHOICES, verbose_name='Vaqt')
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, verbose_name='Kurs')
    preferred_days_of_week = ArrayField(
        models.CharField(max_length=10), verbose_name='Kunlar')
    registered_by = models.ForeignKey(
        Admin, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=20, verbose_name='Raqam')
    phone_number2 = models.CharField(
        max_length=20, blank=True, verbose_name='Raqam 2')
    registered_time = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)


class AlertMessages(models.Model):
    MESSAGES = (
        ('new_group', 'Yangi guruh ochish kerak'),
        ('applicant', 'yangi kelganlarga tel qilish kerak'),
        ('missed_student', 'kelmagan guruhlar tel qilish kerak'),

    )
    to = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={
                           'groups__name__in': ['Admin', 'teacher']}, related_name='messages_to')
    ffrom = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={
                              'groups__name__in': ['teacher', 'boshliq']}, related_name='messages_from')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True)
    message = models.CharField(max_length=255, choices=MESSAGES)
    status = models.CharField(
        max_length=255, choices=STATUS, default='uncompleted')

    