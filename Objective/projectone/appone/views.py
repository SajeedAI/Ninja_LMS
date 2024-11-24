from django.shortcuts import render, get_object_or_404
from .models import Question

def quiz_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        selected_option = request.POST.get('quizOption')
        correct_option = question.options.filter(is_correct=True).first()
        is_correct = correct_option and str(correct_option.id) == selected_option
        return render(request, 'quiz_result.html', {'is_correct': is_correct, 'correct_option': correct_option})
    
    return render(request, 'quiz.html', {'question': question})
