from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ShortLink
from .utils import generate_short_code
from django.contrib.auth.models import User



def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user_links = ShortLink.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'links': user_links})

@login_required
def create_short_link(request):
    if request.method == 'POST':
        original_url = request.POST['original_url']
        short_code = generate_short_code()
        while ShortLink.objects.filter(short_code=short_code).exists():
            short_code = generate_short_code()
        ShortLink.objects.create(user=request.user, original_url=original_url, short_code=short_code)
        return redirect('dashboard')
    return render(request, 'create_link.html')

def redirect_to_original(request, short_code):
    try:
        link = ShortLink.objects.get(short_code=short_code)
        link.click_count += 1  # Увеличиваем счётчик
        link.save()  # Сохраняем изменения
        return redirect(link.original_url)
    except ShortLink.DoesNotExist:
        return render(request, '404.html', status=404)
