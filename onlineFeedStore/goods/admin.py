from django.contrib import admin
from goods.models import Categories, Products
from django_mptt_admin.admin import DjangoMpttAdmin


@admin.register(Categories)
class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", ]


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "price", "quantity"]
    list_editable = [
        "quantity",
        "price",
    ]
    search_fields = ["name"]
    list_filter = ["category"]
