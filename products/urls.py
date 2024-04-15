from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('article/<int:id>/', views.article, name='article'),
]