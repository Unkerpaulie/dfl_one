from django.db.models import Q
from core.models import Currency
from setup.models import CurrencyStock
from transactions.models import Transaction


def get_currency_balance(currency):
    currency_adjustments = CurrencyStock.objects.filter(currency=currency)
    total_adjustment = [c.adjustment_type * c.amount for c in currency_adjustments] 
    return sum(total_adjustment)

def get_blotter_data(currency, blotter_date):
    # currency = Currency.objects.get(id=currency_id)
    num_transactions = Transaction.objects.filter(foreign_currency=currency, contract_date=blotter_date).count()
    opening_adjustments = CurrencyStock.objects.filter(currency=currency, effective_date__lt=blotter_date)
    today_adjustments = CurrencyStock.objects.filter(currency=currency, effective_date=blotter_date)
    future_adjustments = CurrencyStock.objects.filter(currency=currency, effective_date__gt=blotter_date)
    opening = [c.adjustment_type * c.amount for c in opening_adjustments]
    today_purchase = [c.amount for c in today_adjustments if c.adjustment_type == 1]
    today_sale = [c.amount for c in today_adjustments if c.adjustment_type == -1]
    closing = sum(opening) + sum(today_purchase) - sum(today_sale)
    future_purchase = [c.amount for c in future_adjustments if c.adjustment_type == 1]
    future_sale = [c.amount for c in future_adjustments if c.adjustment_type == -1]
    adjusted_closing = closing + sum(future_purchase) - sum(future_sale)
    return {
        "currency": currency,
        "symbol": "", # currency.symbol,
        'opening': sum(opening),
        'today_purchase': sum(today_purchase),
        'today_sale': sum(today_sale),
        'closing': closing,
        'future_purchase': sum(future_purchase),
        'future_sale': sum(future_sale),
        'adjusted_closing': adjusted_closing,
        'num_transactions': num_transactions
    }

def get_register_data(currency):
    transactions = Transaction.objects.filter(currency=currency)

def get_blotter_details(currency, blotter_date):
    opening_adjustments = CurrencyStock.objects.filter(currency=currency, effective_date__lt=blotter_date)
    today_adjustments = CurrencyStock.objects.filter(currency=currency, effective_date=blotter_date)
    future_adjustments = CurrencyStock.objects.filter(currency=currency, effective_date__gt=blotter_date)
    t_list = Transaction.objects.filter(Q(pk__in=today_adjustments.values_list("source_transaction", flat=True)) | Q(pk__in=future_adjustments.values_list("source_transaction", flat=True))).order_by("id")
    opening = sum([c.adjustment_type * c.amount for c in opening_adjustments])
    details = []
    closing = opening
    adj_closing = opening
    for t in t_list:
        record = {}
        record["opening"] = closing
        record["id"] = t.id
        record["client"] = t.client
        record["trader"] = t.trader
        record["contract_date"] = t.contract_date
        record["entry_time"] = t.created_at.time()
        record["rate"] = t.foreign_currency_rate
        record["purchase"] = t.foreign_amount if t.transaction_type == "P" and t.value_date == blotter_date else 0
        record["sale"] = t.settlement_amount if t.transaction_type == "S" and t.value_date == blotter_date else 0
        record["closing"] = closing + record["purchase"] - record["sale"]
        record["future_purchase"] = t.foreign_amount if t.transaction_type == "P" and t.value_date != blotter_date else 0
        record["future_sale"] = t.settlement_amount if t.transaction_type == "S" and t.value_date != blotter_date else 0
        record["adj_closing"] = adj_closing + record["future_purchase"] - record["future_sale"]
        closing = record["closing"]
        adj_closing = record["adj_closing"]

        details.append(record)
    return details

