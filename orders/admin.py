from django.contrib import admin
from .models import Table, Order, OrderItem, Report

admin.site.register(Table)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Report)
