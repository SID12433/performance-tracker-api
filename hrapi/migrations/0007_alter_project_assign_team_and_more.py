# Generated by Django 4.2.5 on 2024-02-29 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrapi', '0006_alter_teams_teamlead'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_assign',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrapi.teams'),
        ),
        migrations.AlterField(
            model_name='project_assign',
            name='teamlead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrapi.teamlead'),
        ),
    ]