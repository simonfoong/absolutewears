from django.urls import path, include

from .views import logout_view, account, user_orders, user_orderdetail

urlpatterns = [
  
    path('logout/', logout_view, name='logout'),
    path('my-account/', account, name='account'),
 
    path('user-orders/', user_orders, name='user_orders'),
    path('order-details/<int:id>/', user_orderdetail, name='user_orderdetail'),

   
]
