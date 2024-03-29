# Generated by Django 4.2 on 2023-04-26 07:37

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='payment',
            name='received_by',
        ),
        migrations.RemoveField(
            model_name='student',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='course',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='last_name',
        ),
        migrations.AddField(
            model_name='group',
            name='duration',
            field=models.CharField(choices=[('1', '1 soat'), ('1.5', '1 soat 30 daqiqa'), ('2', '2 soat')], default='1.5', verbose_name='dars davomiyligi'),
        ),
        migrations.AddField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(related_name='groups', to='home.student'),
        ),
        migrations.AddField(
            model_name='group',
            name='teacher',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('online', 'Online')], default='cash', max_length=10),
        ),
        migrations.AddField(
            model_name='student',
            name='birth_place',
            field=models.CharField(blank=True, max_length=100, verbose_name="Tug'lgan joy"),
        ),
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='student',
            name='first_name',
            field=models.CharField(default='Default first name', max_length=30, verbose_name='Ism'),
        ),
        migrations.AddField(
            model_name='student',
            name='last_name',
            field=models.CharField(default='Default last name', max_length=30, verbose_name='Familiya'),
        ),
        migrations.AddField(
            model_name='student',
            name='phone_number',
            field=models.CharField(default='Default phone', max_length=20, verbose_name='Raqam'),
        ),
        migrations.AddField(
            model_name='student',
            name='phone_number2',
            field=models.CharField(blank=True, max_length=20, verbose_name='Raqam 2'),
        ),
        migrations.AddField(
            model_name='student',
            name='registered_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='course',
            name='teacher',
        ),
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.course', verbose_name='Kurs'),
        ),
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.CharField(default=0, max_length=30),
        ),
        migrations.CreateModel(
            name='TeacherAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('present', models.BooleanField()),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.admin')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('present', models.BooleanField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.student')),
            ],
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='Ism')),
                ('last_name', models.CharField(max_length=30, verbose_name='Familiya')),
                ('birth_place', models.CharField(blank=True, max_length=100, verbose_name="Tug'lgan joy")),
                ('preferred_time', models.CharField(choices=[('morning', 'Abetdan oldin'), ('afternoon', 'Abetdan keyin'), ('anytime', "Farqi yo'q")], max_length=10, verbose_name='Vaqt')),
                ('preferred_days_of_week', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), size=None, verbose_name='Kunlar')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Raqam')),
                ('phone_number2', models.CharField(blank=True, max_length=20, verbose_name='Raqam 2')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('registered_time', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.course', verbose_name='Kurs')),
                ('registered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.admin')),
                ('students', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student', to='home.student')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='admin',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='home.admin'),
        ),
        migrations.AddField(
            model_name='student',
            name='applicant',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='application_student', to='home.applicant'),
        ),
        migrations.AddField(
            model_name='student',
            name='registered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.admin', verbose_name='admin'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ManyToManyField(to='home.teacher'),
        ),
    ]
