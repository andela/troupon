from django.contrib import admin

from models import Advertiser, Category, Deal, Review


class DealAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class AdvertiserAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Deal, DealAdmin)
admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review)
