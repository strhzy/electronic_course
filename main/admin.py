from django.contrib import admin
from import_export.admin import ExportMixin
from django.urls import path
from django.shortcuts import redirect
from django.contrib.admin import ModelAdmin, register
from django.contrib import messages
from django.conf import settings
import subprocess
import os
from django.http import HttpResponse
from .models import *
import csv

@admin.register(BackupFile)
class BackupFileAdmin(ModelAdmin):
    list_display = ("file", "created_at")
    actions = ["restore_backup"]

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        """Добавляем кастомный URL для создания бэкапа."""
        urls = super().get_urls()
        custom = [
            path(
                "make-backup/",
                self.admin_site.admin_view(self.make_backup_view),
                name="make_backup",
            ),
        ]
        return custom + urls

    def make_backup_view(self, request):
        """Создаёт бэкап через pg_dump и сохраняет в модель."""
        try:
            backup_dir = os.path.join(settings.BASE_DIR, "backups")
            os.makedirs(backup_dir, exist_ok=True)

            filename = "backup.dump"
            dest = os.path.join(backup_dir, filename)

            db = settings.DATABASES["default"]
            db_url = (
                f"postgresql://{db['USER']}:{db['PASSWORD']}@"
                f"{db['HOST']}:{db['PORT']}/{db['NAME']}"
            )

            cmd = [
                "pg_dump",
                f"--dbname={db_url}",
                "--format=custom",
                "-f", dest,
            ]

            subprocess.run(cmd, check=True)

            BackupFile.objects.create(file=os.path.join(settings.BASE_DIR, "backups", filename))

            messages.success(request, "Бэкап успешно создан!")

        except subprocess.CalledProcessError:
            messages.error(request, "Ошибка: pg_dump завершился неудачно.")
        except Exception as e:
            messages.error(request, f"Ошибка: {e}")

        return redirect("admin:main_backupfile_changelist")

    def restore_backup(self, request, queryset):
        """Восстанавливает БД из выбранного бэкапа."""
        try:
            if queryset.count() != 1:
                self.message_user(request, "Выберите один бэкап!", messages.ERROR)
                return

            backup = queryset.first()
            backup_path = backup.file.path

            if not os.path.exists(backup_path):
                self.message_user(request, "Файл бэкапа не найден!", messages.ERROR)
                return

            db = settings.DATABASES["default"]
            db_url = (
                f"postgresql://{db['USER']}:{db['PASSWORD']}@"
                f"{db['HOST']}:{db['PORT']}/{db['NAME']}"
            )

            cmd = [
                "pg_restore",
                f"--dbname={db_url}",
                "--clean",
                "--if-exists",
                backup_path,
            ]

            subprocess.run(cmd, check=True)

            self.message_user(request, "База данных успешно восстановлена!", messages.SUCCESS)

        except subprocess.CalledProcessError:
            self.message_user(request, "Ошибка: pg_restore завершился неудачно.", messages.ERROR)

        except Exception as e:
            self.message_user(request, f"Ошибка восстановления: {e}", messages.ERROR)

    restore_backup.short_description = "Восстановить БД из выбранного бэкапа"

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
    list_display = ('id', 'customer', 'comment', 'delivery_address')
    search_fields = ('delivery_address','customer')
    inlines = [OrderItemInline]
    fieldsets = (
        (None, {
            'fields': ('customer', 'comment', 'delivery_address')
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