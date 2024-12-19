from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.db.models import Q
from core.utils import get_blotter_data, get_currency_balance, get_blotter_details
from .models import Currency
from transactions.models import Transaction
from setup.models import CurrencyStock


# home page is consolidated blotter
@login_required
def home(req):
    currencies = Currency.objects.all().exclude(currency_code="TTD")
    tt_currency = Currency.objects.filter(currency_code="TTD").first()
    ttd_on_hand = get_currency_balance(tt_currency)
    today_date = date.today()
    context = {"page_title": f"Consolidated Blotter - {today_date.strftime('%d %b, %Y')}"}
    context["section"] = "home"
    context["ttd_on_hand"] = ttd_on_hand
    context["today_date"] = today_date
    # currency, opening balance, today's purchases, today's sales, pending purchases, pending sales, current balance, 
    context["currency_data"] = []
    for currency in currencies:
        # currency_data = model_to_dict(currency)
        # currency_data["balance"] = get_currency_balance(currency.id)
        # context["currency_data"].append(currency_data)
        context["currency_data"].append(get_blotter_data(currency, today_date))

    # sum_total_value = 6516565 + ttd_on_hand
    # context |= {"ttd_on_hand": ttd_on_hand, "today_date": today_date, "sum_total_value": sum_total_value}

    return render(req, "core/home.html", context)

@login_required
def blotter_detail(req, currency_code):
    currency = Currency.objects.filter(currency_code=currency_code.upper()).first()
    today_date = date.today()
    context = {"page_title": f"{currency_code.upper()} Blotter - {today_date.strftime('%d %b, %Y')}"}
    context["section"] = "home"
    context["details"] = get_blotter_details(currency, today_date)
    return render(req, "core/blotter_table.html", context)


@login_required
def register(req, currency_code):
    currencies = Currency.objects.all().exclude(currency_code="TTD")
    currency = Currency.objects.filter(currency_code=currency_code.upper()).first()
    if not currency:
        messages.warning(req, "Currency not found")
        return redirect("core:home")
    today_date = date.today()
    transactions = Transaction.objects.filter(
        Q(contract_date=today_date), (Q(settlement_currency=currency) | Q(foreign_currency=currency)))
    context = {"page_title": f"{currency_code.upper()} Register - {today_date.strftime('%d %b, %Y')}"}
    context["section"] = "register"
    context["selected_currency"] = currency_code.upper()
    context["transactions"] = transactions
    context["currencies"] = currencies
    return render(req, "core/register_table.html", context)
   

@login_required
def register_all(req):
    currencies = Currency.objects.all().exclude(currency_code="TTD")
    today_date = date.today()
    transactions = Transaction.objects.filter(contract_date=today_date)
    context = {"page_title": f"All Register - {today_date.strftime('%d %b, %Y')}"}
    context["section"] = "register"
    context["selected_currency"] = "ALL"
    context["transactions"] = transactions
    context["currencies"] = currencies
    return render(req, "core/register_table.html", context)


@login_required
def temp_home(req):
    context = {"page_title": "Consolidated Blotter"}
    context["section"] = "home"
    ttd_on_hand = 15032100
    today_date = date.today()
    tempdata = [
        {"name": "USD", "symbol": "$", "open": 1250000, "today_purchases": 14000, "today_sales": 6500, "pending_purchases": 2000, "pending_sales": 1000, "weighted_rate": 6.75342},
        {"name": "EUR", "symbol": "€", "open": 445000, "today_purchases": 2000, "today_sales": 62000, "pending_purchases": 1000, "pending_sales": 5000, "weighted_rate": 7.42251},
        {"name": "GBP", "symbol": "£", "open": 102000, "today_purchases": 500, "today_sales": 200, "pending_purchases": 0, "pending_sales": 0, "weighted_rate": 8.75301},
        {"name": "CAN", "symbol": "$", "open": 393000, "today_purchases": 1500, "today_sales": 0, "pending_purchases": 500, "pending_sales": 1200, "weighted_rate": 4.88612},
    ]
    
    for currency in tempdata:
        currency["balance"] = currency["open"] + currency["today_purchases"] - currency["today_sales"]
        currency["adjusted_balance"] = currency["balance"] + currency["pending_purchases"] - currency["pending_sales"]
        currency["total_value"] = currency["balance"] * currency["weighted_rate"]
    sum_total_value = sum([currency["total_value"] for currency in tempdata]) + ttd_on_hand
    context["data"] = tempdata
    context |= {"ttd_on_hand": ttd_on_hand, "today_date": today_date, "sum_total_value": sum_total_value}
    return render(req, "core/temp_home.html", context)

@login_required
def test(req):
    return render(req, "core/test.html")

@login_required
def forms(req):
    context = {"page": "forms"}
    return render(req, "core/forms.html", context)

