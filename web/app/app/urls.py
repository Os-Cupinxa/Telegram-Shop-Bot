from django.urls import path, include

urlpatterns = [
    path('', include('frontend.urls')),  # Incluir as URLs do frontend
]
