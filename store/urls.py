from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
        path('', views.homei,name='home'),
        path('filter_brand/<int:id>/',views.filter_brand,name='filter_brand'),
        path('filter_phone/<int:id>/',views.filter_phone,name='filter_phone'),
        path('view_all/',views.view_all,name='view_all'),


        path('category/<slug:brand_slug>/<slug:phone_name_slug>/<slug:product_slug>/', views.product_details,name='product_details'),
        path('cart/', views.cart ,name='cart'),
        path('addcart/<int:product_id>/', views.addcart,name='addcart'),
        path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart,name='remove_cart'),
        path('remove_items/<int:product_id>/<int:cart_item_id>/', views.remove_items,name='remove_items'),
        
] + static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)