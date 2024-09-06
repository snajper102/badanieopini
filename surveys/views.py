from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Survey, Question, SurveyResponse, Answer
from django.shortcuts import render
import pandas as pd



def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = Question.objects.filter(survey=survey).order_by('id')

    # Paginator do paginacji pytań
    paginator = Paginator(questions, 5)  # 5 pytań na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Ustal postęp wypełniania ankiety
    progress = int((page_obj.number / paginator.num_pages) * 100)

    if request.method == 'POST':
        # Pobierz odpowiedzi na pytania i zapisz je
        survey_response, created = SurveyResponse.objects.get_or_create(
            survey=survey,
            session_key=request.session.session_key  # Unikalne dla każdej sesji użytkownika
        )

        for question in page_obj:
            answer_data = request.POST.get(f'question_{question.id}')
            if answer_data:  # Sprawdź, czy użytkownik odpowiedział na pytanie
                Answer.objects.update_or_create(
                    question=question,
                    survey_response=survey_response,
                    defaults={'text_answer': answer_data}
                )

        # Obsługa przekierowania na następną stronę
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()
            # Przekierowanie z odpowiednim numerem strony
            return redirect(f'/surveys/survey/{survey_id}/?page={next_page_number}')
        else:
            # Zakończ ankietę, przekieruj do strony z podziękowaniami
            return redirect('thank_you')
    range_10 = range(1, 11)
    return render(request, 'surveys/survey_detail.html', {
        'survey': survey,
        'page_obj': page_obj,
        'progress': progress,
        'range_10': range_10,
    })




def thank_you(request):
        # Przekazujemy listę konfetti z obliczonymi wartościami 'left' i 'animation_delay' do szablonu
        confetti_range = [{'left': (i * 20) % 100, 'animation_delay': i * 0.1} for i in range(50)]
        return render(request, 'surveys/thank_you.html', {'confetti_range': confetti_range})
def survey_results(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    responses = SurveyResponse.objects.filter(survey=survey)
    return render(request, 'surveys/survey_results.html', {'survey': survey, 'responses': responses})

def survey_list(request):
    surveys = Survey.objects.all()  # Pobieranie wszystkich ankiet
    return render(request, 'surveys/survey_list.html', {'surveys': surveys})
