# Generated by Django 4.2.5 on 2024-03-17 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrapi', '0013_remove_performance_assign_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance_assign',
            name='employee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hrapi.employee'),
        ),
    ]
