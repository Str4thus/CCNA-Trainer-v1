from django.db import models

# Create your models here.
class Question(models.Model):
    question_number = models.IntegerField() # Not the ID, its the number which stands at the beginning of each question
    question_type = models.CharField(max_length=50)
    question_text = models.CharField(max_length=500)

    has_image = models.BooleanField(default=False)
    image_url = models.CharField(max_length=200)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

