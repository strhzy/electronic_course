from django.contrib import admin
from import_export.admin import ExportMixin
from django.contrib import admin
from django.http import HttpResponse
from .models import Category, Manufacturer, Product, Customer, Review, Order, OrderItem, Log
import csv

@admin.action(description="Экспортировать выбранные объекты в CSV")
def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response

@admin.register(Log)
class LogAdmin(admin.ModelAdmin, ExportMixin):
    list_display = ('created_at', 'message', 'table')
    search_fields = ('created_at', 'table')
    list_filter = ('table',)
    ordering = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('created_at', 'message', 'table')
        }),
    )
    actions = [export_as_csv]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
    )

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'website')
    search_fields = ('name', 'country')
    list_filter = ('country',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'country', 'website')
        }),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'manufacturer', 'price', 'is_exists')
    search_fields = ('name', 'description')
    list_filter = ('category', 'manufacturer', 'is_exists')
    ordering = ('name',)
    list_editable = ('price', 'is_exists')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'photo', 'is_exists')
        }),
        ('Связи', {
            'fields': ('category', 'manufacturer')
        }),
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('last_name',)
    ordering = ('last_name', 'first_name')
    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone', 'address')
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'rating', 'created_at')
    search_fields = ('product__name', 'customer__email', 'comment')
    list_filter = ('rating', 'created_at', 'product')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('product', 'customer', 'rating', 'comment', 'created_at')
        }),
    )
    readonly_fields = ('created_at',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('product', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer_firstname', 'buyer_surname', 'comment', 'delivery_address')
    search_fields = ('buyer_firstname', 'buyer_surname', 'delivery_address')
    inlines = [OrderItemInline]
    fieldsets = (
        (None, {
            'fields': ('buyer_firstname', 'buyer_surname', 'comment', 'delivery_address')
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('product__name', 'order__id')
    list_filter = ('order',)
    ordering = ('order',)
    fieldsets = (
        (None, {
            'fields': ('order', 'product', 'quantity')
        }),
    )