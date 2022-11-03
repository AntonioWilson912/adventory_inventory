from django.urls import path
from . import views

app_name = 'vendors'

urlpatterns = [
    path('', views.all_vendors, name='all_vendors'),
    path('<int:vendor_id>', views.view_vendor, name='view_vendor'),
    path('new', views.new_vendor_form, name='new_vendor_form'),
    path('add_vendor_to_db', views.add_vendor_to_db),
    path('<int:vendor_id>/edit', views.edit_vendor, name='edit_vendor'),
    path('<int:vendor_id>/update', views.update_vendor),
    path('<int:vendor_id>/delete', views.delete_vendor)
]