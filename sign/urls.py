from django.contrib.auth.views import LoginView, LogoutView

from . import views
from django.urls import path

urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('verification/', views.verification, name='verification'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
]
