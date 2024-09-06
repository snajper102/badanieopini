from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):
    SURVEY_SCALE = 'scale'
    SURVEY_TEXT = 'text'
    SURVEY_YES_NO = 'yesno'
    SURVEY_CHOICE = 'choice'
    SURVEY_TYPES = [
        (SURVEY_SCALE, 'Scale (1-10)'),
        (SURVEY_TEXT, 'Open Text'),
        (SURVEY_YES_NO, 'Yes/No'),
        (SURVEY_CHOICE, 'Multiple Choice'),
    ]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=10, choices=SURVEY_TYPES, default=SURVEY_TEXT)

    def __str__(self):
        return self.text


class SurveyResponse(models.Model):  # Zmieniona nazwa z Response na SurveyResponse
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f"Response to {self.survey.title} on {self.created_at}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    survey_response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE)
    rating_answer = models.IntegerField(null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)
    yes_no_answer = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Answer to {self.question.text}"
