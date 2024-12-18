from django.urls import path
from .views import (
    register, login_view, logout_view, dashboard,
    create_short_link, redirect_to_original, home
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create/', create_short_link, name='create_link'),
    path('<str:short_code>/', redirect_to_original, name='redirect_to_original'),
]
