from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']  # Enlevé 'created_at'
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    # list_filter = ['created_at']  # Commenté car le champ n'existe pas

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'category', 'stock', 'rating_rate']
    list_filter = ['category']  # Enlevé 'created_at'
    search_fields = ['title', 'description']
    list_editable = ['price', 'stock']
    # readonly_fields = ['created_at', 'updated_at']  # Commenté car les champs n'existent pas
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'description', 'price', 'category', 'stock')
        }),
        ('Images', {
            'fields': ('image', 'image_url')
        }),
        ('Évaluations', {
            'fields': ('rating_rate', 'rating_count')
        }),
        # ('Métadonnées', {  # Commenté car les champs n'existent pas
        #     'fields': ('created_at', 'updated_at'),
        #     'classes': ('collapse',)
        # }),
    )
