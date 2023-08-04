from django.contrib import admin

from .models import Products


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'title', 'link', 'price', 'description', 'image_url', 'discount', 'date']
    readonly_fields = ['date']
    list_filter = ['date']
    ordering = ['-date']
