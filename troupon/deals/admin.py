from django.contrib import admin
from .models import Deal, Advertiser, Category


class DealAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Deal, DealAdmin)
admin.site.register(Advertiser)
admin.site.register(Category, CategoryAdmin)
