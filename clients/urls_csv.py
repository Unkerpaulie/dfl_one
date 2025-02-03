from django.urls import path, include
from . import views

app_name = "clients"


urlpatterns = [
    path('', views.home, name="home"),
    path('<int:client_id>/beneficiaries/', views.beneficiaries, name="beneficiaries"),
    path('<int:client_id>/beneficiaries/new/', views.new_beneficiary, name="new_beneficiary"),
    path('<int:client_id>/beneficiaries/<int:beneficiary_id>/edit/', views.edit_beneficiary, name="edit_beneficiary"),
]
