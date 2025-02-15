from django.contrib import admin
from .models import *

admin.site.register(ClientList)
admin.site.register(IndividualClient)
admin.site.register(CorporateClient)
admin.site.register(IdentificationInfo)
admin.site.register(BeneficiaryBank)
admin.site.register(ClientLocalBank)
