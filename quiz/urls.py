from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_view, name='quiz'),
    path('answer/<int:question_id>/', views.answer_view, name='answer'),  # This URL should match the button link
    path('reset/', views.reset_quiz, name='reset_quiz'),
]
