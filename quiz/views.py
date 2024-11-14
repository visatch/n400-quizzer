from django.shortcuts import render, get_object_or_404
from .models import Question

def quiz_view(request):
    question = Question.objects.order_by('?').first()  # Select a random question
    context = {'question': question}
    return render(request, 'quiz/quiz.html', context)

def answer_view(request, question_id):
    question = get_object_or_404(Question, question_id=question_id)
    return render(request, 'quiz/answer.html', {'question': question})
