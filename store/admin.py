from django.contrib import admin

from . models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('category_name',)}
  list_display = ('category_name', 'slug')

  filter_horizontal= ()
  list_filter= ()
  fieldsets= ()

admin.site.register(Category,CategoryAdmin)



class sub_CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('sub_categoryname',)}
  list_display = ('sub_categoryname', 'slug')

admin.site.register(Sub_Category,sub_CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('product_name', 'price','stock','brand','modified_date','is_available',)


class VariationAdmin(admin.ModelAdmin):

  list_display = ('product','variation_category','variation_value', 'is_active',)
  list_editable = ('is_active',)
  list_filter   =  ('product','variation_category','variation_value', 'is_active',)

class CartAdmin(admin.ModelAdmin):
   list_display = ('cart_id','date_added')

class CartitemsAdmin(admin.ModelAdmin):
   list_display = ('product','cart','quantity','is_active',)   


   admin.site.register(Product,ProductAdmin)   
# admin.site.register(Variation,VariationAdmin) 
# admin.site.register(Cart,CartAdmin)   
# admin.site.register(Cartitems,CartitemsAdmin)   
# admin.site.register(Filter_Price)   
# admin.site.register(wishlist)   
# admin.site.register(ReviewRating)   