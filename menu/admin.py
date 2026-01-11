from django.contrib import admin
from .models import Category, MenuItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name',)
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display  = ('name', 'category', 'price', 'is_available')
    list_filter   = ('category', 'is_available')
    search_fields = ('name',)
    ordering      = ('category__name', 'name') 
