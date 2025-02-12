from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ShortLink, ClickStats
from .utils import generate_short_code, get_geo_info
from django.contrib.auth.models import User
import user_agents

def home(request):
    # Если пользователь уже авторизован, перенаправляем его на дашборд
    if request.user.is_authenticated:
        return redirect('dashboard')
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

    # Добавляем статистику по кликам
    links_with_stats = []
    for link in user_links:
        # Получаем статистику по кликам для каждой ссылки
        click_stats = ClickStats.objects.filter(short_link=link).values('country', 'city',
                                                                        'ip_address', 'clicked_at','os','browser')

        # Добавляем информацию о кликах и ссылке в общий список
        links_with_stats.append({
            'link': link,
            'click_stats': click_stats,
            'total_clicks': link.click_count,  # Общее количество кликов
        })

    return render(request, 'dashboard4.html', {'links_with_stats': links_with_stats})


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
        # Получаем IP-адрес пользователя
        ip = request.META.get('REMOTE_ADDR', '')
        # Определяем страну и город
        country, city = get_geo_info(ip)
        # Извлекаем данные из user-agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        print(user_agent)
        parsed_agent = user_agents.parse(user_agent)
        print(parsed_agent.browser)

        browser = f"{parsed_agent.browser.family} {parsed_agent.browser.version_string}"
        os = f"{parsed_agent.os.family} {parsed_agent.os.version_string}"
        print(browser)
        print(os)
        # Сохраняем статистику перехода
        ClickStats.objects.create(
            short_link=link,
            country=country,
            city=city,
            ip_address=ip,
            browser=browser,
            os=os
        )

        # Обновляем счетчик кликов
        link.click_count += 1
        link.save()

        return redirect(link.original_url)
    except ShortLink.DoesNotExist:
        return render(request, '404.html', status=404)
