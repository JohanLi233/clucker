from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import LogInForm, SignUpForm, PostForm
from django.contrib import messages
from .models import User, Post;
from django.views import generic

class UserListView(generic.ListView):
    model = User
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# def new_post(request):
#     return render(request, 'feed.html')


def show_user(request, user_id):
    user = User.objects.filter(id=user_id)
    #reverse('show_user', kwargs={'user_id': id})
    return render(request, 'show_user.html')

def home(request):
    return render(request, 'home.html')

def users(request):
    list = UserListView
    return render(request, 'user_list.html', {'ListView': list})

def feed(request):
    form = PostForm()
    return render(request, 'feed.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')
