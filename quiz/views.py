import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question

def quiz_view(request):
    # Get the list of already shown question IDs from the session
    shown_questions = request.session.get('shown_questions', [])

    # If there's a current question ID in the session, retrieve it
    current_question_id = request.session.get('current_question_id')
    if current_question_id:
        # Fetch the current question to display
        question = Question.objects.get(question_id=current_question_id)
    else:
        # If no current question, fetch a new random question that hasn’t been shown yet
        remaining_questions = Question.objects.exclude(question_id__in=shown_questions)
        if not remaining_questions.exists():
            # If no questions left, redirect to the end or reset page
            return render(request, 'quiz/end.html', {'message': 'All questions have been shown. Please reset to reshuffle.'})
        
        question = random.choice(remaining_questions)

        # Update session with the new current question
        shown_questions.append(question.question_id)
        request.session['shown_questions'] = shown_questions
        request.session['current_question_id'] = question.question_id
        request.session.modified = True  # Ensure session is saved

    # Calculate the shuffle status
    total_questions = Question.objects.count()
    questions_left = total_questions - len(shown_questions)
    current_status = f"{len(shown_questions)}/{total_questions} questions shown"

    context = {
        'question': question,
        'status': current_status,
        'questions_left': questions_left
    }
    return render(request, 'quiz/quiz.html', context)

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

def reset_quiz(request):
    # Clear the session to reset shown questions and current question
    request.session['shown_questions'] = []
    request.session.pop('current_question_id', None)  # Remove the current question ID
    return redirect('quiz')