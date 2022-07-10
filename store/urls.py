from django.urls import path, include
from store import views
urlpatterns = [
    path('store/', views.StoreView.as_view(), name='store'),
    path('shop-category/<int:id>/<slug:slug>',
         views.StoreCategoryView.as_view(), name='category_products'),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='add_to_cart'),
    path('item/<int:id>/<slug:slug>',
         views.product_detail, name='product_detail'),
    path('product/addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('shopcart/', views.shopcart, name='shopcart'),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='add_to_cart'),
    path('deletefromcart/<int:id>/',views. deletefromcart, name='deletefromcart'),
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),





    path('getspinner/', views.getspinner, name='getspinner'),
    
]