from django.contrib import admin
from .models import Transaction, CurrencyStock

class CurrencyStockAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'currency', 'adjustment_source', 'adjustment_type', 'amount', 'entered_by')
    list_filter = ('currency', 'adjustment_source', 'adjustment_type')
    search_fields = ('comment', 'currency__currency_code')
    date_hierarchy = 'created_at'

admin.site.register(Transaction)
admin.site.register(CurrencyStock, CurrencyStockAdmin)
