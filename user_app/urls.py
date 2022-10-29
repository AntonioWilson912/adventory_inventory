from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='root'),
    path('register', views.register_user),
    path('login', views.login_user),
    path('reset_password', views.reset_password_page, name='reset_pass'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('users', views.all_users, name='all_users'),
    path('users/new', views.new_user_form, name='new_user'),
    path('users/<int:user_id>/edit', views.edit_user, name='edit_user'),
    path("logout", views.logout, name='logout')
]