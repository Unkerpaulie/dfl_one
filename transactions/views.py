from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Transaction
from clients.models import Client, BeneficiaryBank
from core.models import Currency, DealStatus
from setup.models import CurrencyStock


# Create your views here.
@login_required
def transactions_list(req):
    if req.user.role == "admin":
        transactions = Transaction.objects.all()
    else:
        transactions = Transaction.objects.all().exclude(client=Client.objects.get(pk=0))
        
    context = {"page_title": "Transactions List"}
    context["transactions"] = transactions
    context["section"] = "transactions"
    return render(req, "transactions/transactions_list.html", context)

@login_required
def new_transaction(req, client_id):
    client = Client.objects.get(pk=client_id)
    # beneficiaries = BeneficiaryBank.objects.filter(client=client)
    beneficiaries = client.beneficiaries.all()
    transaction_types = Transaction.transaction_types
    currencies = Currency.objects.all()
    deal_statuses = DealStatus.objects.all()
    context = {"page_title": f"New Transaction for {client.ClientName}"}
    context["section"] = "transactions"
    context["client"] = client
    context["beneficiaries"] = beneficiaries
    context |= {"transaction_types": transaction_types, "currencies": currencies, "deal_statuses": deal_statuses}
    try:
        context["deal_id"] = Transaction.objects.latest("id").id + 1 
    except:
        context["deal_id"] = 1 # if no transactions exist yet


    if req.method == "POST":        
        contract_date = req.POST.get("contract_date")
        value_date = req.POST.get("value_date")
        transaction_type = req.POST.get("transaction_type")
        settlement_currency = int(req.POST.get("settlement_currency"))
        settlement_currency_rate = float(req.POST.get("settlement_currency_rate"))
        settlement_amount = req.POST.get("settlement_amount")
        origin_currency = int(req.POST.get("origin_currency"))
        origin_currency_rate = float(req.POST.get("origin_currency_rate"))
        origin_amount = req.POST.get("origin_amount")
        beneficiary = int(req.POST.get("beneficiary"))
        deal_status = int(req.POST.get("deal_status"))

        transaction = Transaction(
            client=client, 
            contract_date=contract_date, 
            value_date=value_date, 
            transaction_type=transaction_type, 
            settlement_currency=Currency.objects.get(id=settlement_currency),
            settlement_currency_rate=settlement_currency_rate, 
            settlement_amount=settlement_amount, 
            origin_currency=Currency.objects.get(id=origin_currency), 
            origin_currency_rate=origin_currency_rate, 
            origin_amount=origin_amount, 
            deal_status=DealStatus.objects.get(id=deal_status), 
            trader=req.user, 
            beneficiary=BeneficiaryBank.objects.get(id=beneficiary)
        )
        transaction.save()
        # update currency stock
        # deduct settlement currency amount from currency stock
        decrease_stock = CurrencyStock(
            source_transaction=transaction,
            currency=Currency.objects.get(id=settlement_currency),
            currency_rate=settlement_currency_rate,
            amount=settlement_amount,
            effective_date=value_date,
            adjustment_source = "X",
            adjustment_type = -1,
            entered_by=req.user,
            last_updated_by=req.user
        )
        decrease_stock.save()
        # add origin currency amount to currency stock
        increase_stock = CurrencyStock(
            source_transaction=transaction,
            currency=Currency.objects.get(id=origin_currency),
            currency_rate=origin_currency_rate,
            amount=origin_amount,
            effective_date=value_date,
            adjustment_source = "X",
            adjustment_type = 1,
            entered_by=req.user,
            last_updated_by=req.user
        )
        increase_stock.save()
        
        messages.success(req, "Transaction added successfully")
        return redirect("transactions:transactions_list")
    return render(req, "transactions/transactions_form.html", context)

@login_required
def edit_transaction(req, client_id, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    client = transaction.client
    beneficiaries = client.beneficiaries.all()
    transaction_types = Transaction.transaction_types
    currencies = Currency.objects.all()
    deal_statuses = DealStatus.objects.all()
    context = {"page_title": f"Edit Transaction for {client.ClientName}"}
    context["section"] = "transactions"
    context["client"] = client
    context["transaction"] = transaction
    context["beneficiaries"] = beneficiaries
    context |= {"transaction_types": transaction_types, "currencies": currencies, "deal_statuses": deal_statuses}
    context["deal_id"] = transaction_id
    context["formdata"] = {
        "contract_date": transaction.contract_date,
        "value_date": transaction.value_date,
        "transaction_type": transaction.transaction_type,
        "settlement_currency": transaction.settlement_currency,
        "settlement_currency_rate": transaction.settlement_currency_rate,
        "settlement_amount": transaction.settlement_amount,
        "origin_currency": transaction.origin_currency,
        "origin_currency_rate": transaction.origin_currency_rate,
        "origin_amount": transaction.origin_amount,
        "deal_status": transaction.deal_status,
        "beneficiary": transaction.beneficiary
    }

    if req.method == "POST":
        contract_date = req.POST.get("contract_date")
        value_date = req.POST.get("value_date")
        transaction_type = req.POST.get("transaction_type")
        settlement_currency = int(req.POST.get("settlement_currency"))
        settlement_currency_rate = float(req.POST.get("settlement_currency_rate"))
        settlement_amount = req.POST.get("settlement_amount")
        origin_currency = int(req.POST.get("origin_currency"))
        origin_currency_rate = float(req.POST.get("origin_currency_rate"))
        origin_amount = req.POST.get("origin_amount")
        deal_status = int(req.POST.get("deal_status"))
        beneficiary = int(req.POST.get("beneficiary"))
        
        transaction.contract_date = contract_date
        transaction.value_date = value_date
        transaction.transaction_type = transaction_type
        transaction.settlement_currency = Currency.objects.get(id=settlement_currency)
        transaction.settlement_currency_rate = settlement_currency_rate
        transaction.settlement_amount = settlement_amount
        transaction.origin_currency = Currency.objects.get(id=origin_currency)
        transaction.origin_currency_rate = origin_currency_rate
        transaction.origin_amount = origin_amount
        transaction.deal_status = DealStatus.objects.get(id=deal_status)
        # transaction.trader = req.user
        transaction.beneficiary = BeneficiaryBank.objects.get(id=beneficiary)
        transaction.save()
        # update currency stock decrease
        decrease_stock = CurrencyStock.objects.filter(source_transaction=transaction, adjustment_type=-1).first()
        decrease_stock.currency=Currency.objects.get(id=settlement_currency)
        decrease_stock.currency_rate=settlement_currency_rate
        decrease_stock.amount=settlement_amount
        decrease_stock.effective_date=value_date
        decrease_stock.last_updated_by=req.user
        decrease_stock.save()
        # update currency stock increase
        increase_stock = CurrencyStock.objects.filter(source_transaction=transaction, adjustment_type=1).first()
        increase_stock.currency=Currency.objects.get(id=origin_currency)
        decrease_stock.currency_rate=origin_currency_rate
        increase_stock.amount=origin_amount
        increase_stock.effective_date=value_date
        increase_stock.last_updated_by=req.user
        increase_stock.save()
        messages.success(req, "Transaction updated successfully")
        return redirect("transactions:transactions_list")
    return render(req, "transactions/transactions_form.html", context)


def ajax_beneficiary(req, client_id, beneficiary_id):
    beneficiary = BeneficiaryBank.objects.filter(pk=beneficiary_id)
    data = serializers.serialize("json", beneficiary)
    return JsonResponse(data, safe=False)