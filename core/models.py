from django.db import models

# no longer in use
class IdentificationType(models.Model):
    id_type = models.CharField(max_length=40)

    def __str__(self):
        return self.id_type
    
    
class Currency(models.Model):
    currency_name = models.CharField(max_length=140)
    currency_code = models.CharField(max_length=5)
    symbol = models.CharField(max_length=1, default="$", blank=True)

    class Meta:
        verbose_name_plural = "currencies"

    def __str__(self):
        return f"{self.currency_code}"


class DealStatus(models.Model):
    status_name = models.CharField(max_length=140)

    class Meta:
        verbose_name_plural = "deal statuses"

    def __str__(self):
        return self.status_name
    

class Country(models.Model):
    country = models.CharField(max_length=200)
    country_code = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = "Countries"
        
    def __str__(self):
        return self.country

