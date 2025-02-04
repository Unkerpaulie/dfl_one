from django.urls import path
from . import views

app_name = "setup"


urlpatterns = [
    path('restricted/', views.non_admin_redirect, name="restricted"),
    path('users/', views.list_users, name="list_users"),
    path('users/add/', views.add_user, name="add_user"),
    path('users/<int:user_id>/reset/', views.reset_user_password, name="reset_user_password"),
    path('users/<int:user_id>/edit/', views.edit_user, name="edit_user"),
    path('deal_statuses/', views.list_deal_status, name="list_deal_status"),
    path('deal_statuses/add/', views.add_deal_status, name="add_deal_status"),
    path('deal_statuses/<int:deal_status_id>/edit/', views.edit_deal_status, name="edit_deal_status"),
    path('identification_types/', views.list_identification_types, name="list_identification_types"),
    path('identification_types/add/', views.add_identification_type, name="add_identification_type"),
    path('identification_types/<int:identification_type_id>/edit/', views.edit_identification_type, name="edit_identification_type"),
    path('currencies/', views.list_currencies, name="list_currencies"),
    path('currencies/add/', views.add_currency, name="add_currency"),
    path('currencies/<int:currency_id>/edit/', views.edit_currency, name="edit_currency"),
    path('inventory/', views.show_currency_inventory, name="show_currency_inventory"),
    path('inventory/<int:currency_id>/adjust/', views.adjust_currency, name="adjust_currency"),
    path('bank_fee/', views.update_bank_fee, name="update_bank_fee"),
]
