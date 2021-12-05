from django.urls import path, include
from .views import register_view, login_view, logout_view, username_validate_view, home_view, password_reset_request, password_reset_confirm, welcome_view
from django.contrib.auth import views as auth_views #import this
from .forms import CustomSetPasswordForm

urlpatterns = [
    path('', welcome_view, name="welcome-view"),
    path('register/', register_view, name="register-view"),
    path('login/', login_view, name="login-view"),
    path('logout/', logout_view, name="logout-view"),
    path('validateuser/', username_validate_view, name="username-validate-view"),
    path('home/', home_view, name="home-view"),
    path('welcome/', welcome_view, name="welcome-view"),
    # path('/', home_view, name="home-view"),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    # path('reset/<uidb64>/<token>/', password_reset_confirm(form_class=CustomSetPasswordForm, template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),              
    path("password_reset/", password_reset_request, name="password_reset")
]


