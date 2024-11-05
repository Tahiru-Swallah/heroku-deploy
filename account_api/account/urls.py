from django.urls import path
from .views import LoginView, RegistrationView, MyPublicView, Api_Root, PasswordChangeView

urlpatterns = [
    path('api-root/', Api_Root.as_view(), name='api_root'),
    path('login/', LoginView.as_view(), name='login_api'),
    path('sgnup/', RegistrationView.as_view(), name='signup_api'),
    path('my_public_api/',MyPublicView.as_view(), name='mypublicapi'),
    path('change_password/',PasswordChangeView.as_view(), name='change_password_api'),
]