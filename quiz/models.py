from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.TextField()
    answer_text = models.TextField()
    question_id = models.IntegerField(unique=True)
    
    def __str__(self):
        return self.question_text
