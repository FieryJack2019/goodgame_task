from django.urls import path
from . import views


urlpatterns = [
    path('user/', views.UserDetail.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
    path('users/<int:gameId>/', views.UserList.as_view()),
    path('user-add/', views.UserCreate.as_view()),
    path('game/<int:pk>/', views.GameDetail.as_view()),
    path('games/<int:categoryId>/', views.GameList.as_view()),
    path('category/', views.CategoryList.as_view()),
]