from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name = 'index'),
    path('add-to-cart/',addtocart,name = "addtocart"),
    path('delete-from-cart/',deletefromcart,name="deletefromcart"),
    path('update-cart/',updatecart,name="updatecart"),
    path('add-to-wishlist/',addtowishlist,name = "addtowishlist"),
    path('product-details/<int:pk>/',productdetails,name="productdetails"),
    path('products/',products,name="products"),
    path('wishlist/',wishlist,name="wishlist"),
    path('cart/',cart,name="cart"),
    path('shop/<str:x>/',shop,name="shop"),
    path('shoppagedata/',shoppagedata,name="shoppagedata"),
    path('getshippingquote/',getshippingquote,name="getshippingquote"),
    path('applycoupon/',applycoupon,name="applycoupon"),
    path('checkout/',checkout,name="checkout"),
    path('place-order/',placeorder,name="placeorder"),
    path('order-placed/',orderplaced,name="orderplaced"),
    path('contact-us/',contactus,name="contactus"),
    path('send-contact-query/',sendcontactquery,name="sendcontactquery"),
    path('thank-you/',thankyou,name="thankyou"),
    path('register/',register,name="register"),
]
