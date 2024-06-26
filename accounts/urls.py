from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("<int:id>/profile/", views.profile, name="profile"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("update_nickname/", views.update_nickname, name="update_nickname"),
    path("<int:id>/follow/", views.follow, name="follow"),
    path('<int:id>/like_article/', views.like_article, name='like_article'),
]
