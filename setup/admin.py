from django.contrib import admin
from .models import BankFee, DFLLocalBank, DFLInternationalBank

admin.site.register(BankFee)
admin.site.register(DFLLocalBank)
admin.site.register(DFLInternationalBank)