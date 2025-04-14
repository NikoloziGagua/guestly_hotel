from django.contrib import admin
from .models import FoodItem, FoodOrder, FoodOrderItem, ServiceRequest

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'room', 'request_type', 'status', 'created_at')
    list_filter = ('status', 'request_type', 'created_at')
    search_fields = ('guest__username', 'room__room_number', 'description')
@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(FoodOrder)
class FoodOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'room', 'ordered_at', 'status')
    search_fields = ('guest__username', 'room__room_number')

@admin.register(FoodOrderItem)
class FoodOrderItemAdmin(admin.ModelAdmin):
    list_display = ('food_order', 'food_item', 'quantity')
