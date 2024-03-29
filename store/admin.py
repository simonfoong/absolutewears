from django.contrib import admin
import admin_thumbnails
from mptt.admin import DraggableMPTTAdmin
from .models import Product, ShopCart, Color, Size, Variants, Images, Category, Comment
# Register your models here.


# class CategoryAdmin2(DraggableMPTTAdmin):
#     mptt_indent_field = "title"
#     list_display = ('tree_actions', 'indented_title',
#                     'related_products_count', 'related_products_cumulative_count')
#     list_display_links = ('indented_title',)
#     prepopulated_fields = {'slug': ('title',)}

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)

#         # Add cumulative product count
#         qs = Category.objects.add_related_count(
#             qs,
#             Product,
#             'category',
#             'products_cumulative_count',
#             cumulative=True)

#         # Add non cumulative product count
#         qs = Category.objects.add_related_count(qs,
#                                                 Product,
#                                                 'category',
#                                                 'products_count',
#                                                 cumulative=False)
#         return qs

#     def related_products_count(self, instance):
#         return instance.products_count
#     related_products_count.short_description = 'Related products (for this specific category)'

#     def related_products_cumulative_count(self, instance):
#         return instance.products_cumulative_count
#     related_products_cumulative_count.short_description = 'Related products (in tree)'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['spec', 'title']
    list_filter = ['spec']
    # prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('slug',)


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'price', 'amount']
    list_filter = ['user']


@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1



class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True



@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'image_thumbnail']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_tag']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline, ProductVariantsInline]
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment']

    readonly_fields = ('subject', 'comment', 'user', 'ip')


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'color',
                    'size', 'price', 'quantity', 'image_tag']




admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(Comment, CommentAdmin)
