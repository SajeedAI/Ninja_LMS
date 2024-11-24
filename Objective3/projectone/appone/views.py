from django.shortcuts import render, get_object_or_404, redirect
from .models import Week, Question, Option, UserResponse
from django.contrib.auth.decorators import login_required

@login_required
def test_overview(request):
    print("test_overview: ")
    """Show all available weeks with tests."""
    weeks = Week.objects.all()
    return render(request, 'test_overview.html', {'weeks': weeks})

@login_required
def take_test(request, week_id):
    print("take_test: ")
    """Show questions for a specific week and allow users to answer."""
    week = get_object_or_404(Week, id=week_id)
    questions = week.questions.all()

    if request.method == 'POST':
        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            is_correct = selected_option == question.correct_option
            UserResponse.objects.create(
                question=question,
                selected_option=selected_option,
                is_correct=is_correct
            )
        return redirect('test_results', week_id=week.id)

    return render(request, 'take_test.html', {'week': week, 'questions': questions})

@login_required
def test_results(request, week_id):
    print("test_results: ")
    """Show the results for a specific week."""
    responses = UserResponse.objects.filter(question__week_id=week_id)
    total_questions = responses.count()
    correct_answers = responses.filter(is_correct=True).count()
    incorrect_answers = total_questions - correct_answers

    return render(request, 'test_results.html', {
        'responses': responses,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
    })

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')  # This is a sample page for authenticated users

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.shortcuts import render
from .models import Week

@login_required
def available_tests(request):
    # Fetch all the weeks (available tests)
    weeks = Week.objects.all()  # Assuming you have a Week model that holds test data
    
    # Render the template with the weeks context
    return render(request, 'available_tests.html', {'weeks': weeks})

@login_required
def profile_view(request):
    # You can fetch user-specific data if needed, or just render the profile page
    return render(request, 'profile.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login
def custom_login(request):
    print("Login")
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', '/test_overview')  # Redirect to 'next' or home page
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.contrib.auth import logout
# Custom logout view
def custom_logout(request):
    print("custom_logout: ")
    logout(request)  # Logs the user out
    return redirect('login')  # Redirect to login page or home page