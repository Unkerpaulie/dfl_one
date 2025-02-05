from django.urls import path, include
from . import views

app_name = "clients"


urlpatterns = [
    path('', views.home, name="home"),
    path('i/new/', views.new_individual, name="new_individual"),
    path('i/<int:client_id>/', views.edit_individual, name="edit_individual"),
    path('c/new/', views.new_corporate, name="new_corporate"),
    path('c/<int:client_id>/', views.edit_corporate, name="edit_corporate"),
    path('i/<int:client_id>/beneficiaries/', views.beneficiaries_i, name="beneficiaries_i"),
    path('c/<int:client_id>/beneficiaries/', views.beneficiaries_c, name="beneficiaries_c"),
    path('i/<int:client_id>/beneficiaries/new/', views.new_i_beneficiary, name="new_i_beneficiary"),
    path('c/<int:client_id>/beneficiaries/new/', views.new_c_beneficiary, name="new_c_beneficiary"),
    path('i/<int:client_id>/beneficiaries/<int:beneficiary_id>/', views.edit_i_beneficiary, name="edit_i_beneficiary"),
    path('c/<int:client_id>/beneficiaries/<int:beneficiary_id>/', views.edit_c_beneficiary, name="edit_c_beneficiary"),
    # path('<int:client_id>/beneficiaries/<int:beneficiary_id>/edit/', views.edit_beneficiary, name="edit_beneficiary"),
]
