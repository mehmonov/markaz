# Generated by Django 4.2 on 2023-04-30 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_student_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='present',
        ),
        migrations.AddField(
            model_name='admin',
            name='status',
            field=models.CharField(choices=[('completed', "o'qishni tugatdan"), ('uncompleted', "o'qishni tugatmagan")], default='uncompleted', verbose_name='status admin'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.course'),
        ),
        migrations.AddField(
            model_name='group',
            name='status',
            field=models.CharField(choices=[('completed', "o'qishni tugatdan"), ('uncompleted', "o'qishni tugatmagan")], default='uncompleted', verbose_name='status group'),
        ),
        migrations.AddField(
            model_name='student',
            name='status',
            field=models.CharField(choices=[('completed', "o'qishni tugatdan"), ('uncompleted', "o'qishni tugatmagan")], default='uncompleted', verbose_name='status student'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='status',
            field=models.CharField(choices=[('completed', "o'qishni tugatdan"), ('uncompleted', "o'qishni tugatmagan")], default='uncompleted', verbose_name='status teacher'),
        ),
        migrations.AlterField(
            model_name='group',
            name='teacher',
            field=models.IntegerField(),
        ),
    ]
