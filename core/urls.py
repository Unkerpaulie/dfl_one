from django.urls import path, include
from . import views

app_name = "core"


urlpatterns = [
    path('', views.home, name="home"),
    path('test/', views.test, name="test"),
    path('register/', views.register_all, name="register_all"),
    path('forms/', views.forms, name="forms"),
]
