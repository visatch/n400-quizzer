from django.core.management.base import BaseCommand
from quiz.models import Question

class Command(BaseCommand):
    help = 'Loads questions and answers from separate files into the database'

    def handle(self, *args, **kwargs):
        questions_file_path = "quiz/static/quiz/civic-100-questions.txt"
        answers_file_path = "quiz/static/quiz/civic-100-answers.txt"
        qa_index = set()                       # To track loaded IDs and avoid duplicates

        def load_questions(file_path):
            questions = {}
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line and line[0].isdigit():
                        parts = line.split(". ", 1)
                        question_id = int(parts[0])  # ID as integer
                        question_text = parts[1] if len(parts) > 1 else ""
                        questions[question_id] = question_text  # Store question by ID
            return questions

        def load_answers(file_path):
            answers = {}
            current_id = None
            current_answer = ""

            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()

                    # Check if line starts with an ID, indicating a new answer entry
                    if line and line[0].isdigit():
                        # Store the current answer if an ID was being processed
                        if current_answer and current_id not in qa_index:
                            answers[current_id] = current_answer.strip()
                            qa_index.add(current_id)

                        # Extract ID and initialize a new answer
                        parts = line.split(". ", 1)
                        current_id = int(parts[0])  # ID as integer
                        current_answer = parts[1] if len(parts) > 1 else ""
                    else:
                        # Continue appending to the current answer if it spans multiple lines
                        current_answer += " " + line

                # Add the last answer if it exists
                if current_answer and current_id not in qa_index:
                    answers[current_id] = current_answer.strip()
                    qa_index.add(current_id)

            return answers

        # Load questions and answers from files
        questions = load_questions(questions_file_path)
        answers = load_answers(answers_file_path)

        # Save questions and answers to the database
        for q_id, question_text in questions.items():
            answer_text = answers.get(q_id, "Answer not provided.")
            Question.objects.update_or_create(
            question_id=q_id,
            defaults={
                'question_text': question_text,
                'answer_text': answer_text,
        }
    )

        self.stdout.write(self.style.SUCCESS('Questions and answers loaded successfully.'))
