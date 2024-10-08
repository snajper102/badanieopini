# Generated by Django 4.2.16 on 2024-09-05 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0003_response_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_answer', models.IntegerField(blank=True, null=True)),
                ('text_answer', models.TextField(blank=True, null=True)),
                ('yes_no_answer', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.survey')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('scale', 'Scale (1-10)'), ('text', 'Open Text'), ('yesno', 'Yes/No'), ('choice', 'Multiple Choice')], default='text', max_length=10),
        ),
        migrations.DeleteModel(
            name='Response',
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='survey_response',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.surveyresponse'),
        ),
    ]
