from django.contrib import admin
from . import models
from .models import OrderItem,Order
class ClientAdmin(admin.ModelAdmin):
    list_display=['user','phone','email']
    list_filter=['user','email']
    search_fields=['user','phone','email']
class OrderItemAdmin(admin.TabularInline):
    model=OrderItem
    raw_id_fields = ['product']
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','total_price','date','paid','ordered',)
    list_filter=['user','paid','paid']
    search_fields=('user','paid',)
    actions = ('paid_true',)
    def paid_true(self, request, queryset):
        count = queryset.update(paid=True)
        self.message_user(request, f"{count} paid successfully")
    inlines = [
	OrderItemAdmin,
	]
class OrderItem2Admin(admin.ModelAdmin):
    list_display=['user','total_price']
admin.site.register(models.Client,ClientAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(OrderItem,OrderItem2Admin)
admin.site.register(models.ProductAlternative)