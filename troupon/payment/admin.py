from django.contrib import admin

from payment.models import Purchases


# Register your models here.
class PurchasesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Purchases, PurchasesAdmin)
