from django.urls import path
from .views import survey_list, survey_detail, survey_results, thank_you
from . import views

urlpatterns = [
    path('', survey_list, name='survey_list'),
    path('survey/<int:survey_id>/', survey_detail, name='survey_detail'),
    path('survey/<int:survey_id>/results/', survey_results, name='survey_results'),
    path('thank-you/', thank_you, name='thank_you'),



]
