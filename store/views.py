from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse,HttpResponse
# Create your views here.


def homei(request):
    products = Product.objects.all().filter(
        is_available=True).order_by('-id')[0:8]
    
    category = Category.objects.all().order_by('-id')[0:8]

    context = {
        'products': products,
        'category':category
    }
    return render(request, 'store_template/index.html', context)


def filter_brand(request,id):
    filter_brand = Sub_Category.objects.filter(category=id)
    context ={
        'filter_brand':filter_brand
    }
    
    return render(request,'store_template/category.html', context)


def filter_phone(request,id):
    product = Product.objects.filter(phone_name=id)
    context ={
        'mobile_phones':product
    }
    return render(request,'store_template/category.html', context)


def view_all(request):
    category = Category.objects.all()
    context ={
        'veiw_all_category':category
    }
    return render(request,'store_template/category.html', context)
    






def product_details(request, brand_slug, phone_name_slug, product_slug):
    try:
        print("my try")
        single_product = Product.objects.get(
            brand__slug=brand_slug, phone_name__slug=phone_name_slug, slug=product_slug)
        related_products = Product.objects.filter(
            phone_name__slug=phone_name_slug)[0:4]

    except Exception as e:
        raise e
    # if request.user.is_authenticated:   
    #     try:
    #         orderproduct = OrderProduct.objects.filter(user=request.user,product_id = single_product.id ).exists()
    #     except OrderProduct.DoesNotExist:
    #         orderproduct = None    
    # else:
        # orderproduct = None 
    # reviews = ReviewRating.objects.filter(product_id = single_product.id ,status = True)     
    context = {
        'single_product': single_product,
        'related_products': related_products,
        # 'orderproduct':orderproduct,
        # 'reviews':reviews,
        
        
    }
    return render(request, 'store_template/shop-details.html', context)






# getting session id
# sessionkey is session id


def _cart_id(request):

    cart = request.session.session_key
    if not cart: # if no session create new one
        cart = request.session.create()
    return cart


def addcart(request, product_id):
    current_user = request.user
    # get the product  #getting session in cart   using cartid
    product = Product.objects.get(id=product_id)

    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                print(key)
                print(value)
                try:
                    variation = Variation.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = Cartitems.objects.filter(
            product=product, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = Cartitems.objects.filter(
                product=product, user=current_user)
            # is the current variation inside the existing variations then increse qnty cart item
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in existing_variation_list:
                # increase cart item quantity
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = Cartitems.objects.get(product=product, id=item_id)
                if (product.stock - item.quantity)>0:
                    item.quantity += 1
                    item.save()
                else:
                    messages.error(request,'No more stock available')
                    return redirect('cart')    


            else:
                item = Cartitems.objects.create(
                    product=product, quantity=1, user=current_user)
                # create new cart item
                # checking product variation empty or not
                if len(product_variation) > 0:
                    item.variations.clear()
                    # cart_item.quantity += 1    # incresing quantinty in cart
                    item.variations.add(*product_variation)
                    print(item)
                    item.save()
        # except Cartitems.DoesNotExist:
        else:
            cart_item = Cartitems.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('cart')

     # if user is not authenticated
    else:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                print(key)
                print(value)
                try:
                    variation = Variation.objects.get(
                        product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            # get cart using cart id present in session
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()
            # putting product inside cart
        is_cart_item_exists = Cartitems.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = Cartitems.objects.filter(product=product, cart=cart)
            # existing variations
            # current variations
            # item_id

            # is the current variation inside the existing variations then increse qnty cart item
            existing_variation_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in existing_variation_list:
                # increase cart item quantity
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = Cartitems.objects.get(product=product, id=item_id)
                if (product.stock - item.quantity)>0:
                    item.quantity += 1
                    item.save()
                else:
                    messages.error(request,'No more stock available')
                    return redirect('cart')    

            else:
                item = Cartitems.objects.create(
                    product=product, quantity=1, cart=cart)
                # create new cart item
                # checking product variation empty or not
                if len(product_variation) > 0:
                    item.variations.clear()
                    # cart_item.quantity += 1    # incresing quantinty in cart
                    item.variations.add(*product_variation)
                    print(item)
                    item.save()
        # except Cartitems.DoesNotExist:
        else:
            cart_item = Cartitems.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = Cartitems.objects.get(product=product, user=request.user, id=cart_item_id)
        else:  
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = Cartitems.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')


def remove_items(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)


    if request.user.is_authenticated:
         cart_item = Cartitems.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = Cartitems.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):

    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = Cartitems.objects.filter(
                user=request.user, is_active=True).order_by('-id')

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitems.objects.filter(cart=cart, is_active=True).order_by('-id')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            print(total)
            quantity += cart_item.quantity
        tax = (3 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,

    }

    return render(request, 'store_template/cart.html', context)