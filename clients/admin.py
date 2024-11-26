from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(ClientType)
admin.site.register(ClientSubType)
admin.site.register(ClientStatus)
admin.site.register(ClientAccountStatus)
admin.site.register(ClientAMLRiskRating)
admin.site.register(Country)
admin.site.register(BeneficiaryBank)
