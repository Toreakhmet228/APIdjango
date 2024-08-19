from django.contrib import admin
from .models import Review,Product,Category
@admin.register(Category)
class data(admin.ModelAdmin):
    pass

@admin.register(Product)
class data(admin.ModelAdmin):
    pass
@admin.register(Review)
class data(admin.ModelAdmin):
    pass