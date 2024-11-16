import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question

def quiz_view(request):
    # Retrieve session variables
    shown_questions = request.session.get('shown_questions', [])
    current_question_id = request.session.get('current_question_id')
    previous_questions = request.session.get('previous_questions', [])

    question = None

    # Validate the `current_question_id`
    if current_question_id:
        try:
            question = Question.objects.get(question_id=current_question_id)
        except Question.DoesNotExist:
            current_question_id = None

    # Handle "Previous Question" button click
    if request.GET.get("previous") == "true" and previous_questions:
        # Remove the current question from `shown_questions` if valid
        if current_question_id and current_question_id in shown_questions:
            shown_questions.remove(current_question_id)

        # Revert to the last question in `previous_questions`
        current_question_id = previous_questions.pop()

        # Add the reverted question back to `shown_questions`
        if current_question_id not in shown_questions:
            shown_questions.append(current_question_id)

        # Update session variables
        request.session['previous_questions'] = previous_questions
        request.session['shown_questions'] = shown_questions
        request.session['current_question_id'] = current_question_id
        request.session.modified = True

        # Fetch the reverted question
        question = Question.objects.get(question_id=current_question_id)

        # Redirect to clean the URL
        return redirect('quiz')

    elif "next_question" in request.POST:  # Handle "Next Question" button click
        # Add the current question to `previous_questions` if valid
        if current_question_id and current_question_id not in previous_questions:
            previous_questions.append(current_question_id)

        # Fetch a new random question
        remaining_questions = Question.objects.exclude(question_id__in=shown_questions)
        if not remaining_questions.exists():
            return render(request, 'quiz/end.html', {'message': 'All questions have been shown. Please reset to reshuffle.'})

        question = random.choice(remaining_questions)
        current_question_id = question.question_id
        shown_questions.append(current_question_id)

    # If `current_question_id` is None, fetch the first random question
    if current_question_id is None:
        remaining_questions = Question.objects.exclude(question_id__in=shown_questions)
        if remaining_questions.exists():
            question = random.choice(remaining_questions)
            current_question_id = question.question_id
            shown_questions.append(current_question_id)
        else:
            return render(request, 'quiz/end.html', {'message': 'All questions have been shown. Please reset to reshuffle.'})

    # Update session variables
    request.session['current_question_id'] = current_question_id
    request.session['shown_questions'] = shown_questions
    request.session['previous_questions'] = previous_questions
    request.session.modified = True

    # Calculate the quiz status
    total_questions = Question.objects.count()
    questions_left = total_questions - len(shown_questions)
    current_status = f"{len(shown_questions)}/{total_questions} questions shown"

    return render(request, 'quiz/quiz.html', {
        'question': question,
        'questions_left': questions_left,
        'status': current_status,
        'can_browse_previous': len(previous_questions) > 0
    })


def next_question(request):
    # Retrieve the current question ID and previous_questions from the session
    current_question_id = request.session.get('current_question_id')
    previous_questions = request.session.get('previous_questions', [])

    # Add the current question to `previous_questions`
    if current_question_id and current_question_id not in previous_questions:
        previous_questions.append(current_question_id)
        request.session['previous_questions'] = previous_questions
        request.session.modified = True  # Ensure session changes are saved

    # Clear the current question ID to allow the next question to be selected
    request.session.pop('current_question_id', None)

    # Redirect to the main quiz view with a clean URL
    return redirect('quiz')

def reset_quiz(request):
    # Clear session data
    request.session['shown_questions'] = []
    request.session.pop('current_question_id', None)
    request.session['previous_questions'] = []
    request.session.modified = True  # Ensure session changes are saved
    return redirect('quiz')


def answer_view(request, question_id):
    # Fetch the question by ID
    question = get_object_or_404(Question, question_id=question_id)

    # Get session variables
    shown_questions = request.session.get('shown_questions', [])
    previous_questions = request.session.get('previous_questions', [])
    current_question_id = request.session.get('current_question_id')

    # Calculate remaining questions
    total_questions = Question.objects.count()
    questions_left = total_questions - len(shown_questions)

    # Render the answer template
    return render(request, 'quiz/answer.html', {
        'question': question,
        'questions_left': questions_left
    })



# 21 10