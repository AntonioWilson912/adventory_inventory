from django.urls import path
from . import views

app_name = 'vendors'

urlpatterns = [
    path('', views.all_vendors, name='all_vendors'),
    path('<int:vendor_id>', views.view_vendor, name='view_vendor'),
    path('new', views.new_vendor_form, name='new_vendor_form'),
    path('<int:vendor_id>/edit', views.edit_vendor, name='edit_vendor')
]