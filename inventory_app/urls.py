from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('<int:product_id>', views.view_product, name='view_product'),
    path('new', views.new_product_form, name='new_product_form'),
    path('<int:product_id>/edit', views.edit_product, name='edit_product')
]