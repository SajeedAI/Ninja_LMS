from django.shortcuts import render, redirect
from .models import Question, Option, UserResponse

def quiz_view(request):
    questions = Question.objects.prefetch_related('options').all()
    return render(request, 'quiz.html', {'questions': questions})

def submit_quiz(request):
    if request.method == 'POST':
        correct_count = 0
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = key.split('_')[1]
                selected_option = value
                question = Question.objects.get(id=question_id)
                if question.correct_option == selected_option:
                    correct_count += 1
        return render(request, 'result.html', {'score': correct_count})
    return redirect('quiz')
