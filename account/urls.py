from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),  
    path('profile/', views.user_profile, name='profile'),  
    path('change_password/', views.change_password, name='change_password'),  
]
