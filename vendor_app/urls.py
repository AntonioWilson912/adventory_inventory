from django.urls import path
from . import views

app_name = 'vendors'

urlpatterns = [
    path('', views.all_vendors),
    path('<int:vendor_id>', views.view_vendor),
    path('new', views.new_vendor_form),
    path('<int:vendor_id>/edit', views.edit_vendor)
]