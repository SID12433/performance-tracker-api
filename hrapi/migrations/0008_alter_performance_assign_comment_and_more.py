# Generated by Django 4.2.5 on 2024-02-29 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrapi', '0007_alter_project_assign_team_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance_assign',
            name='comment',
            field=models.CharField(choices=[('Perfect', 'Perfect'), ('Average', 'Average'), ('Bad', 'Bad')], max_length=50),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='teamlead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrapi.teamlead'),
        ),
        migrations.AlterField(
            model_name='taskchart',
            name='end_date',
            field=models.DateField(),
        ),
    ]
