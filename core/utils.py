from core.models import Currency
from setup.models import CurrencyStock
from transactions.models import Transaction


def get_currency_balance(currency):
    currency_adjustments = CurrencyStock.objects.filter(currency=currency)
    total_adjustment = [c.adjustment_type * c.amount for c in currency_adjustments] 
    return sum(total_adjustment)

def get_blotter_data(currency, blotter_date):
    # currency = Currency.objects.get(id=currency_id)
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
        'adjusted_closing': adjusted_closing
    }

def get_register_data(currency):
    transactions = Transaction.objects.filter(currency=currency)

    
