from django.contrib import admin
from . models import Payment,Order,OrderProduct,Address,Discount,Discount_coupon

# Register your models here.




class OrderAdmin(admin.ModelAdmin):
    list_display = [ 'user','order_total','payment','status','is_ordered','created_at']
    list_per_page: 20
 

class PaymentAdmin(admin.ModelAdmin):
    list_display = [ 'user','payment_id','amount_paid','created_at']
    list_per_page: 20



class OrderProductAdmin(admin.ModelAdmin):
    list_display = [ 'order','payment','user','product','size','product_price','quantity','ordered']
    list_per_page: 20
    

class AddressAdmin(admin.ModelAdmin):
    list_display = [ 'user','first_name','last_name','phone','email','address_line1','country','state','pincode']
    list_per_page: 20

admin.site.register(Payment,PaymentAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Discount)
admin.site.register(Discount_coupon)


