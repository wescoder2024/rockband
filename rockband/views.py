from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Question, Choice
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
# Create your views here.
class blog(generic.ListView):
    queryset= Post.objects.all().order_by("-date")[:25]
    template_name="blog.html"

class Postdetail(generic.DetailView):
    model = Post
    template_name="post.html"

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, "polls/poll.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(
            pk=request.POST['choice']
        )
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(
            reverse('rockband:results', args=(question_id,))
        )

# Send user to login page
def user_login(request):
    return render(request, 'authentication/login.html')

# Check to see if user login details are correct
def authenticate_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponseRedirect(
            reverse('rockband:login')
        )
    else:
        login(request, user)
        return HttpResponseRedirect(
            reverse('rockband:show_user')
        )

# Show user.html page when login is successful
def show_user(request):
    print(request.user.username)
    return render(request, 'authentication/user.html', {
        "username": request.user.username,
        "password": request.user.password
    })

# user registration page
def register(request):
    return render(request, 'authentication/register.html')

# User registration process
def register_user(request):
    username= request.POST['username']
    password= request.POST['password']

    if 'first_name' in request.POST:
        first_name= request.POST['first_name']
    else:
        first_name=''
        last_name=''
        email=''

    user=authenticate(username=username, password=password)
    if user is None:
        user= User.objects.create_user(
            username, first_name, password)
        login(request, user)
        return HttpResponseRedirect(
            reverse('rockband:show_user'))
    else:
        return render(request, 'authentication/register.html', {
            'error_message': "user already exists"
        }) 