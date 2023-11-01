from django.core.serializers import serialize
from django.contrib import admin
from manufacturer.models import Network, Product
from manufacturer.tasks import clear_debt_async
from django.utils.html import format_html


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "city", "supplier_link", "debt")
    list_filter = ("city",)
    actions = ["clear_debt"]

    def supplier_link(self, obj):
        if obj.supplier:
            url = f"/admin/manufacturer/network/{obj.supplier.id}/change/"
            link = f'<a href="{url}">{obj.supplier.name}</a>'
            return format_html(link)
        return "N/A"

    supplier_link.allow_tags = True
    supplier_link.short_description = "Поставщик"

    def clear_debt(modeladmin, request, queryset):
        if queryset.count() > 20:
            serialized_objects = serialize("json", queryset)
            clear_debt_async.delay(serialized_objects)
        else:
            queryset.update(debt=0)

    clear_debt.short_description = "Очистить задолженность перед поставщиком"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date")
