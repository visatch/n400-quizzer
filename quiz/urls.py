from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_view, name='quiz'),
    path('answer/<int:question_id>/', views.answer_view, name='answer'),
    path('next/', views.next_question, name='next_question'),  # New path for next question
    path('reset/', views.reset_quiz, name='reset_quiz'),
]
