from django.contrib import admin

from logistic.models import Product, Stock, StockProduct

# Register your models here.


class StockProductInline(admin.TabularInline):
    model = StockProduct
    extra = 1

class StockAdmin(admin.ModelAdmin):
    inlines = [StockProductInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(StockProduct)

