from django.urls import path
from .views import register_view, login_view, logout_view, username_validate_view, home_view

urlpatterns = [
    # path('', home_view, name='home'),
    path('register/', register_view, name="register-view"),
    path('login/', login_view, name="login-view"),
    path('logout/', logout_view, name="logout-view"),
    path('validateuser/', username_validate_view, name="username-validate-view"),
    path('home/', home_view, name="home-view"),
    # path('create_task/', create_task, name='create-task'),
]
