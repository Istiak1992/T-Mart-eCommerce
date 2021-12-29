from django.urls import path
from .views import *



urlpatterns = [
    path('', homePage, name="homePage"),
    path('<slug:category_slug>',productCategory, name="product_by_category"),
    path('productDetails/<int:pk>/', productDetails, name="productDetails"),
    path('add-to-cart/<int:id>/', AddtoCartView, name="add-to-cart"),
    path('managecart/<int:item_id>/', ManageCart.as_view(), name="managecart"),
    path('checkout/<int:cart_id>/', checkout, name="checkout"),
    path('viewCart/', individualCart, name="viewCart"),
    path('register/', registerRequest, name="register"),
    path('login/', loginRequest, name="login"),
    path('logout/', logoutRequest, name= "logout"),
    path('search/', searchOperation, name="search"),
    path('review/', reviewRate, name="review"),
    path('support/', supportPage, name="supportPage"),

    
   
   
]
