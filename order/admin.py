from django.contrib import admin
import admin_thumbnails
from mptt.admin import DraggableMPTTAdmin
from .models import Order, OrderProduct
# Register your models here.


class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'price', 'quantity', 'amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'phone', 'total', 'status', 'ordered']
    list_filter = ['status', 'ordered']
    readonly_fields = ('user', 'address', 'phone',
                       'first_name', 'ip', 'last_name', 'phone', 'total')
    can_delete = False
    inlines = [OrderProductline]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price', 'quantity', 'amount']
    list_filter = ['user']





admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Order, OrderAdmin)

