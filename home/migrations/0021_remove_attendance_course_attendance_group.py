# Generated by Django 4.2 on 2023-05-10 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_payment_is_confirmed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='course',
        ),
        migrations.AddField(
            model_name='attendance',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.group'),
        ),
    ]