from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    
    # User paths
    path('users/', views.users_list, name='users_list'),
    path('users/add/', views.users_add, name='users_add'),
    path('users/edit/<int:id>/', views.users_edit, name='users_edit'),
    path('users/delete/', views.users_delete, name='users_delete'),
    
    # Product paths
    path('products/', views.products_list, name='products_list'),
    path('products/add', views.product_add, name='product_add'),
    path('products/edit/<int:id>/', views.product_edit, name='product_edit'),
    path('products/delete', views.product_delete, name='product_delete'),

    # Category paths
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/add', views.category_add, name='category_add'),
    path('categories/edit/<int:id>/', views.category_edit, name='category_edit'),
    path('categories/delete', views.category_delete, name='category_delete'),
]
