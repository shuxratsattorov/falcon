from django.contrib import admin

from app import models
from app.models import ProductAttribute, Image, Attribute, AttributeValue, Comment, Profile, Rating

# Register your models here.

admin.site.register(Image)
admin.site.register(ProductAttribute)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Rating)


@admin.register(models.Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'amount', 'discount', 'stock', 'slug']
    prepopulated_fields = {'slug': ('name',)}


# class ImageInline(admin.StackedInline):
#     model = Image
#     form = ImageForm
#     formset = MinimumImageInlineFormSet
#     extra = 1
#
# admin.site.unregister(Product)
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [ImageInline]
