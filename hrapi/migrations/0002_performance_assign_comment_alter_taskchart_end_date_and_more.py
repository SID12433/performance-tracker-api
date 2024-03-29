# Generated by Django 4.2.5 on 2024-02-28 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance_assign',
            name='comment',
            field=models.CharField(choices=[('Perfect', 'Perfect'), ('Average', 'Average'), ('Bad', 'Bad')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='taskchart',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='taskchart',
            name='project_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrapi.projectdetail'),
        ),
    ]
