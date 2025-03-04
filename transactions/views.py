from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Transaction, CurrencyStock
from clients.models import ClientList, BeneficiaryBank, ClientLocalBank
from core.models import Currency, DealStatus
from setup.models import BankFee, DFLLocalBank, DFLInternationalBank


# Create your views here.
@login_required
def transactions_list(req):
    if req.user.role == "admin":
        transactions = Transaction.objects.all()
    else:
        transactions = Transaction.objects.all().exclude(client=ClientList.objects.get(pk=0))
        
    context = {"page_title": "Transactions List"}
    context["transactions"] = transactions
    context["section"] = "transactions"
    return render(req, "transactions/transactions_list.html", context)

@login_required
def new_transaction(req, client_id):
    client = ClientList.objects.get(pk=client_id)
    bank_fee = BankFee.objects.get(pk=1)
    context = {"page_title": f"New Transaction for {client.client_name}"}
    context["section"] = "transactions"
    context["client"] = client
    context["bank_fee"] = bank_fee.bank_fee
    context |= {
        "beneficiaries": client.beneficiaries.all(),
        "local_banks": ClientLocalBank.objects.filter(client=client),
        "inpayment_types": Transaction.INPAYMENT_TYPES,
        "transaction_types": Transaction.TRANSACTION_TYPES, 
        "currencies": Currency.objects.all(), 
        "deal_statuses": DealStatus.objects.all(),  
        "local_banks": DFLLocalBank.objects.all(),
        "intl_banks": DFLInternationalBank.objects.all()
        }
    context["deal_id"] = Transaction.objects.latest("id").id + 1 

    if req.method == "POST":        
        contract_date = req.POST.get("contract_date")
        value_date = req.POST.get("value_date")
        transaction_type = req.POST.get("transaction_type")
        foreign_currency = int(req.POST.get("foreign_currency"))
        foreign_currency_rate = float(req.POST.get("foreign_currency_rate"))
        foreign_amount = req.POST.get("foreign_amount")
        settlement_currency = int(req.POST.get("settlement_currency"))
        settlement_currency_rate = float(req.POST.get("settlement_currency_rate"))
        settlement_amount = float(req.POST.get("settlement_amount"))
        bank_fee = float(req.POST.get("bank_fee"))
        deal_status = int(req.POST.get("deal_status"))
        # inbound payment options to DFL
        in_payment_type = req.POST.get("in_payment_type")
        check_number = req.POST.get("check_number")
        dfl_local_bank_account = int(req.POST.get("dfl_local_bank_account")) if req.POST.get("in_payment_type") == "local" else None
        dfl_intl_bank_account = int(req.POST.get("dfl_intl_bank_account")) if req.POST.get("in_payment_type") == "foreign" else None
        # out_payment values: cash, fixed, bb-, lb-
        out_payment = req.POST.get("out_payment") # not saved in model
        cash_settlement = out_payment == "cash"
        fixed_deposit = out_payment == "fixed"
        fixed_deposit_cert = req.POST.get("fixed_deposit_cert")
        client_beneficiary_account = BeneficiaryBank.objects.get(id=int(out_payment.split("-")[1])) if out_payment.startswith("bb-") else None
        client_local_bank_account = ClientLocalBank.objects.get(id=int(out_payment.split("-")[1])) if out_payment.startswith("lb-") else None
        payment_details = req.POST.get("payment_details")

        transaction = Transaction(
            client=client, 
            contract_date=contract_date, 
            value_date=value_date, 
            transaction_type=transaction_type, 
            foreign_currency=Currency.objects.get(id=foreign_currency), 
            foreign_currency_rate=foreign_currency_rate, 
            foreign_amount=foreign_amount, 
            settlement_currency=Currency.objects.get(id=settlement_currency),
            settlement_currency_rate=settlement_currency_rate, 
            settlement_amount=settlement_amount, 
            bank_fee=bank_fee, 
            deal_status=DealStatus.objects.get(id=deal_status), 
            # inbound payment options to DFL
            in_payment_type=in_payment_type,
            check_number=check_number,
            dfl_local_bank_account=DFLLocalBank.objects.get(id=dfl_local_bank_account) if dfl_local_bank_account else None,
            dfl_intl_bank_account=DFLLocalBank.objects.get(id=dfl_intl_bank_account) if dfl_local_bank_account else None,
            # outbound payment options to client
            cash_settlement=cash_settlement,
            fixed_deposit=fixed_deposit,
            fixed_deposit_cert=fixed_deposit_cert,
            client_beneficiary_account=client_beneficiary_account,
            client_local_bank_account=client_local_bank_account,
            payment_details=payment_details,
            trader=req.user, 
            last_updated_by=req.user
        )
        transaction.save()
        # update currency stock
        # adjust foreign currency stock
        foreign_stock = CurrencyStock(
            source_transaction=transaction,
            currency=Currency.objects.get(id=foreign_currency),
            currency_rate=foreign_currency_rate,
            amount=foreign_amount,
            effective_date=value_date,
            adjustment_source = "X",
            adjustment_type = 1 if transaction.transaction_type == "P" else -1,
            entered_by=req.user,
            last_updated_by=req.user
        )
        foreign_stock.save()
        # adjust settlement currency stock
        settlement_stock = CurrencyStock(
            source_transaction=transaction,
            currency=Currency.objects.get(id=settlement_currency),
            currency_rate=settlement_currency_rate,
            amount=settlement_amount,
            effective_date=value_date,
            adjustment_source = "X",
            adjustment_type = -1 if transaction.transaction_type == "P" else 1,
            entered_by=req.user,
            last_updated_by=req.user
        )
        settlement_stock.save()
        
        messages.success(req, "Transaction added successfully")
        return redirect("transactions:transactions_list")
    return render(req, "transactions/transactions_form.html", context)

@login_required
def edit_transaction(req, client_id, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    client = transaction.client
    bank_fee = BankFee.objects.get(pk=1)
    context = {"page_title": f"Edit Transaction for {client.client_name}"}
    context["section"] = "transactions"
    context["client"] = client
    context["bank_fee"] = transaction.bank_fee
    context |= {
        "beneficiaries": client.beneficiaries.all(),
        "local_banks": ClientLocalBank.objects.filter(client=client),
        "inpayment_types": Transaction.INPAYMENT_TYPES,
        "transaction_types": Transaction.TRANSACTION_TYPES, 
        "currencies": Currency.objects.all(), 
        "deal_statuses": DealStatus.objects.all(),  
        "local_banks": DFLLocalBank.objects.all(),
        "intl_banks": DFLInternationalBank.objects.all()
        }
    context["deal_id"] = transaction_id

    out_payment = None
    if transaction.cash_settlement:
        out_payment = "cash"
    elif transaction.fixed_deposit:
        out_payment = "fixed"
    elif transaction.client_local_bank_account is not None:
        out_payment = f"lb-{transaction.client_local_bank_account.id}"
    elif transaction.client_beneficiary_account is not None:
        out_payment = f"bb-{transaction.client_beneficiary_account.id}"
    context["formdata"] = transaction

    if req.method == "POST":
        contract_date = req.POST.get("contract_date")
        value_date = req.POST.get("value_date")
        transaction_type = req.POST.get("transaction_type")
        settlement_currency = int(req.POST.get("settlement_currency"))
        settlement_currency_rate = float(req.POST.get("settlement_currency_rate"))
        settlement_amount = float(req.POST.get("settlement_amount"))
        foreign_currency = int(req.POST.get("foreign_currency"))
        foreign_currency_rate = float(req.POST.get("foreign_currency_rate"))
        foreign_amount = req.POST.get("foreign_amount")
        bank_fee = float(req.POST.get("bank_fee"))
        deal_status = int(req.POST.get("deal_status"))
        out_payment = req.POST.get("out_payment")
        cash_settlement = out_payment == "cash"
        fixed_deposit = out_payment == "fixed"
        fixed_deposit_cert = req.POST.get("fixed_deposit_cert")
        client_beneficiary_account = BeneficiaryBank.objects.get(id=int(out_payment.split("-")[1])) if out_payment.startswith("bb-") else None
        client_local_bank_account = ClientLocalBank.objects.get(id=int(out_payment.split("-")[1])) if out_payment.startswith("lb-") else None
        payment_details = req.POST.get("payment_details")
        
        # update transaction data from form
        transaction.contract_date = contract_date
        transaction.value_date = value_date
        transaction.transaction_type = transaction_type
        transaction.foreign_currency = Currency.objects.get(id=foreign_currency)
        transaction.foreign_currency_rate = foreign_currency_rate
        transaction.foreign_amount = foreign_amount
        transaction.settlement_currency = Currency.objects.get(id=settlement_currency)
        transaction.settlement_currency_rate = settlement_currency_rate
        transaction.settlement_amount = settlement_amount
        transaction.bank_fee = bank_fee
        transaction.deal_status = DealStatus.objects.get(id=deal_status)
        # transaction.trader = req.user
        transaction.cash_settlement = cash_settlement
        transaction.fixed_deposit = fixed_deposit
        transaction.fixed_deposit_cert = fixed_deposit_cert
        transaction.client_beneficiary_account = client_beneficiary_account
        transaction.client_local_bank_account = client_local_bank_account
        transaction.payment_details = payment_details
        transaction.last_updated_by = req.user
        transaction.save()

        # update foreign currency stock
        foreign_stock = CurrencyStock.objects.filter(source_transaction=transaction).first()
        foreign_stock.currency=Currency.objects.get(id=settlement_currency)
        foreign_stock.currency_rate=settlement_currency_rate
        foreign_stock.amount=settlement_amount
        foreign_stock.adjustment_type = 1 if transaction_type == "P" else -1
        foreign_stock.effective_date=value_date
        foreign_stock.last_updated_by=req.user
        foreign_stock.save()
        # update settlement currency stock
        settlement_stock = CurrencyStock.objects.filter(source_transaction=transaction).last()
        settlement_stock.currency=Currency.objects.get(id=foreign_currency)
        settlement_stock.currency_rate=foreign_currency_rate
        settlement_stock.amount=foreign_amount
        settlement_stock.adjustment_type = -1 if transaction_type == "P" else 1
        settlement_stock.effective_date=value_date
        settlement_stock.last_updated_by=req.user
        settlement_stock.save()
        messages.success(req, "Transaction updated successfully")
        return redirect("transactions:transactions_list")
    return render(req, "transactions/transactions_form.html", context)


def ajax_beneficiary(req, client_id, beneficiary_id):
    beneficiary = BeneficiaryBank.objects.filter(pk=beneficiary_id)
    data = serializers.serialize("json", beneficiary)
    return JsonResponse(data, safe=False)

def ajax_dfl_bank(req, client_id, bank_account_id):
    bank_account = DFLLocalBank.objects.filter(pk=bank_account_id)
    data = serializers.serialize("json", bank_account)
    return JsonResponse(data, safe=False)

def ajax_client_bank(req, client_id, bank_account_id):
    bank_account = ClientLocalBank.objects.filter(pk=bank_account_id)
    data = serializers.serialize("json", bank_account)
    return JsonResponse(data, safe=False)

