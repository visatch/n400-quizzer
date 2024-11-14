import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question

def quiz_view(request):
    # Retrieve the list of shown question IDs and the current question ID from the session
    shown_questions = request.session.get('shown_questions', [])
    current_question_id = request.session.get('current_question_id')

    # If there’s a current question ID in the session, retrieve the same question
    if current_question_id:
        question = Question.objects.get(question_id=current_question_id)
    else:
        # Fetch a new random question that hasn’t been shown yet
        remaining_questions = Question.objects.exclude(question_id__in=shown_questions)
        
        # If no remaining questions, show end or reset page
        if not remaining_questions.exists():
            return render(request, 'quiz/end.html', {'message': 'All questions have been shown. Please reset to reshuffle.'})
        
        # Select a new question and update the session variables
        question = random.choice(remaining_questions)
        shown_questions.append(question.question_id)
        request.session['shown_questions'] = shown_questions
        request.session['current_question_id'] = question.question_id
        request.session.modified = True  # Ensure session is saved

    # Calculate the remaining questions count and status
    total_questions = Question.objects.count()
    questions_left = total_questions - len(shown_questions)
    current_status = f"{len(shown_questions)}/{total_questions} questions shown"

    context = {
        'question': question,
        'status': current_status,
        'questions_left': questions_left
    }
    return render(request, 'quiz/quiz.html', context)

def next_question(request):
    # Clear the current question ID to allow the next question to be selected
    request.session.pop('current_question_id', None)
    return redirect('quiz')

def reset_quiz(request):
    # Clear the session to reset shown questions and current question
    request.session['shown_questions'] = []
    request.session.pop('current_question_id', None)  # Remove the current question ID
    return redirect('quiz')

def answer_view(request, question_id):
    # Fetch the question by its ID
    question = get_object_or_404(Question, question_id=question_id)

    # Get the list of already shown question IDs from the session
    shown_questions = request.session.get('shown_questions', [])
    total_questions = Question.objects.count()
    questions_left = total_questions - len(shown_questions)

    # Render the answer template, passing the question and questions_left
    return render(request, 'quiz/answer.html', {
        'question': question,
        'questions_left': questions_left
    })
