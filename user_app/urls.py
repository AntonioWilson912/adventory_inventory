from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index),
    path('register', views.register_user),
    path('login', views.login_user),
    path('reset_password', views.reset_password_page),
    path('dashboard', views.dashboard),
    path('users', views.all_users),
    path('users/new', views.new_user_form),
    path('users/<int:user_id>/edit', views.edit_user)
]