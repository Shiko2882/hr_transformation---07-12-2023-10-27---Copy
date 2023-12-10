# Generated by Django 4.2.7 on 2023-12-04 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hr_admin', '0003_inputsform_alter_company_companyinputs_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InputsAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=100)),
                ('notes', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='InputsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='InputsQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('options', models.CharField(blank=True, choices=[('yes_no', 'Yes or No'), ('multiple_choice', 'Multiple Choice'), ('single_choice', 'Single Choice')], max_length=100, null=True)),
                ('notes', models.TextField()),
                ('InputsCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_admin.inputscategory')),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='category',
        ),
        migrations.RemoveField(
            model_name='question',
            name='form',
        ),
        migrations.RenameField(
            model_name='evaluationanswer',
            old_name='question',
            new_name='EvaluationQuestion',
        ),
        migrations.RenameField(
            model_name='evaluationcategory1',
            old_name='evaluationform',
            new_name='EvaluationForm',
        ),
        migrations.RenameField(
            model_name='evaluationcategory2',
            old_name='category',
            new_name='EvaluationCategory1',
        ),
        migrations.RemoveField(
            model_name='evaluationanswer',
            name='CompanyInputs',
        ),
        migrations.RemoveField(
            model_name='inputsform',
            name='notes',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.AddField(
            model_name='inputscategory',
            name='InputsForm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_admin.inputsform'),
        ),
        migrations.AddField(
            model_name='inputsanswer',
            name='InputsQuestion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_admin.inputsquestion'),
        ),
        migrations.AddField(
            model_name='inputsanswer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]