from django.urls import path, include
from . import views

app_name = "transactions"


urlpatterns = [
    path('', views.transactions_list, name="transactions_list"),
    path('<int:client_id>/new/', views.new_transaction, name="new_transaction"),
    path('<int:client_id>/<int:transaction_id>/', views.edit_transaction, name="edit_transaction"),
    path('<int:client_id>/beneficiary/<int:beneficiary_id>', views.ajax_beneficiary, name="ajax_beneficiary"),
    path('<int:client_id>/dfl_bank/<int:bank_account_id>', views.ajax_dfl_bank, name="ajax_beneficiary"),
    path('<int:client_id>/client_bank/<int:bank_account_id>', views.ajax_client_bank, name="ajax_beneficiary"),
]
