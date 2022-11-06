from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('search_products', views.search_products),
    path('<int:product_id>', views.view_product, name='view_product'),
    path('new', views.new_product_form, name='new_product_form'),
    path('add_product_to_db', views.add_product_to_db),
    path('<int:product_id>/add_vendor', views.add_product_vendor),
    path('<int:product_id>/edit', views.edit_product, name='edit_product'),
    path('<int:product_id>/update', views.update_product),
    path("<int:product_id>/update_primary_vendor", views.update_primary_vendor),
    path('<int:product_id>/delete', views.delete_product)
]