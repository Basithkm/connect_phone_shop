from .models import Category,Sub_Category,Cart,Cartitems
from .views import _cart_id

def menu_links(request):
    links = Category.objects.all()
    return dict (links=links)

def imenu_links(request):
    s_links = Sub_Category.objects.all()
    return dict (s_links=s_links)    

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return{}

    else:
        try: 
            cart = Cart.objects.filter(cart_id =_cart_id(request))  
            if request.user.is_authenticated:
                cart_items =Cartitems.objects.all().filter(user=request.user)
            else:    
                cart_items = Cartitems.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity   
        except Cart.DoesNotExist:
            cart_count = 0
    return dict (cart_count=cart_count)          