from django.urls import path, include
from . import views

app_name = "transactions"


urlpatterns = [
    path('', views.transactions_list, name="transactions_list"),
    path('<int:client_id>/new/', views.new_transaction, name="new_transaction"),
    path('<int:client_id>/<int:transaction_id>/edit/', views.edit_transaction, name="edit_transaction"),
    path('<int:client_id>/beneficiary/<int:beneficiary_id>', views.ajax_beneficiary, name="ajax_beneficiary"),
]