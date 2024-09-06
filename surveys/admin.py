from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Survey, Question, SurveyResponse, Answer
from django.http import HttpResponse
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Użycie backendu "Agg" do generowania wykresów bez GUI
matplotlib.use('Agg')

# Klasa Inline do wyświetlania odpowiedzi
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    max_num = None
    min_num = 0
    readonly_fields = ('question', 'rating_answer', 'text_answer', 'yes_no_answer')  # Tylko do odczytu
    can_delete = False  # Brak możliwości usuwania odpowiedzi z poziomu inline
    fields = ('question', 'rating_answer', 'text_answer', 'yes_no_answer')  # Wyświetl tylko te pola


def generate_survey_charts():
    # Pobierz wszystkie odpowiedzi na ankiety
    answers = Answer.objects.all()

    # Grupa przykładów: Zlicz odpowiedzi na pytanie o ocenę jakości obsługi
    question_data = {}
    for answer in answers:
        if answer.question.text not in question_data:
            question_data[answer.question.text] = []
        # Dodaj odpowiedź do listy
        if answer.rating_answer is not None:
            question_data[answer.question.text].append(answer.rating_answer)

    # Tworzenie wykresów na podstawie danych
    chart_paths = []
    for question, data in question_data.items():
        # Generowanie wykresu dla każdej grupy pytań
        plt.figure(figsize=(10, 6))
        plt.hist(data, bins=10, alpha=0.7, color='blue')
        plt.title(f'Odpowiedzi na pytanie: {question}')
        plt.xlabel('Ocena')
        plt.ylabel('Liczba odpowiedzi')

        # Konwersja wykresu do obrazu base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plot_base64 = base64.b64encode(image_png).decode('utf-8')
        chart_paths.append(plot_base64)
        plt.close()

    return chart_paths

# Funkcja do eksportu odpowiedzi do CSV
def export_survey_responses_to_csv(modeladmin, request, queryset):
    # Przygotowanie danych do Pandas DataFrame
    data = []
    for response in queryset:
        response_data = {
            'Response ID': response.id,
            'Survey Title': response.survey.title,
            'Date': response.created_at,
        }
        answers = Answer.objects.filter(survey_response=response)
        for answer in answers:
            response_data[answer.question.text] = answer.rating_answer or answer.text_answer or answer.yes_no_answer
        data.append(response_data)

    # Tworzenie DataFrame za pomocą Pandas
    df = pd.DataFrame(data)

    # Tworzenie pliku CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="survey_responses.csv"'
    df.to_csv(path_or_buf=response, index=False)

    return response

export_survey_responses_to_csv.short_description = "Export selected responses to CSV"

# Admin dla SurveyResponse z wykresem analizy
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'created_at')
    inlines = [AnswerInline]  # Tutaj używamy AnswerInline, który musi być wcześniej zdefiniowany
    actions = [export_survey_responses_to_csv]

    # Metoda do wyświetlania wykresu analizy
    def changelist_view(self, request, extra_context=None):
        # Pobieranie danych do wykresu
        responses = SurveyResponse.objects.all()
        survey_titles = [response.survey.title for response in responses]
        response_counts = [SurveyResponse.objects.filter(survey=response.survey).count() for response in responses]

        # Generowanie wykresu
        plt.figure(figsize=(10, 6))
        plt.bar(survey_titles, response_counts)
        plt.title('Ilość odpowiedzi dla każdej ankiety')
        plt.xlabel('Ankieta')
        plt.ylabel('Ilość odpowiedzi')

        # Konwersja wykresu na obraz base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plot_base64 = base64.b64encode(image_png).decode('utf-8')

        # Dodanie wykresu do kontekstu
        extra_context = extra_context or {}
        extra_context['plot_base64'] = plot_base64
        extra_context['title'] = "Wykres analizy ankiety"

        return super().changelist_view(request, extra_context=extra_context)





# Rejestracja modelu SurveyResponse w panelu admina
admin.site.register(SurveyResponse, SurveyResponseAdmin)

# Standardowa rejestracja dla innych modeli
admin.site.register(Survey)
admin.site.register(Question)
