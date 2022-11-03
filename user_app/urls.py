from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='root'),
    path('register', views.register_user),
    path('login', views.login_user),
    path('reset_password', views.reset_password_page, name='reset_pass'),
    path('reset_password_in_db', views.reset_password_in_db),
    path('dashboard', views.dashboard, name='dashboard'),
    path('users', views.all_users, name='all_users'),
    path('users/new', views.new_user_form, name='new_user'),
    path('users/create_user_in_db', views.create_user_in_db),
    path('users/<int:user_id>/edit', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/update_user_in_db', views.update_user_in_db),
    path("users/<int:user_id>/delete", views.delete_user),
    path("logout", views.logout, name='logout')
]