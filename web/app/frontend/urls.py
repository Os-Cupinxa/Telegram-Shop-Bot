from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login', views.login_view, name='login'),
    path('l', views.logout_view, name='logout'),
    
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

    # Client paths
    path('clients/', views.clients_list, name='clients_list'),
    path('clients/edit/<int:id>/', views.client_edit, name='client_edit'),
    #path('clients/delete', views.client_delete, name='client_delete'),

    # Broadcast paths
    # Broadcast path
    path('broadcast/', views.broadcast_message, name='broadcast'),

    #path('broadcast/send', views.broadcast_send, name='broadcast_add'),

    # Order paths
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/edit/<int:id>/', views.order_edit, name='order_edit'),
    
    # Conversations path
    path('conversations/', views.conversations_list, name='conversations_list'),
    path('conversations/<int:chat_id>/', views.conversation_messages, name='conversation_messages'),
    path('conversations/<int:chat_id>/mark_as_read/', views.mark_conversation_as_read, name='mark_conversation_as_read'),

]
