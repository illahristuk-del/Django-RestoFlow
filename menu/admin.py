from django.contrib import admin
from .models import Category, Dish, ModifierGroup, Modifier

admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(ModifierGroup)
admin.site.register(Modifier)