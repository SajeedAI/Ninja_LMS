from django.db import models

class Question(models.Model):
    text = models.TextField()
    program = models.TextField(blank=True, null=True)  # Optional program content
    correct_option = models.CharField(max_length=1)  # 'a', 'b', 'c', 'd'

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    option_value = models.CharField(max_length=1)  # 'a', 'b', 'c', 'd'

    def __str__(self):
        return self.option_text

class UserResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"Response to Question {self.question.id}"
