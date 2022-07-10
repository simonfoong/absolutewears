from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .models import Userprofile
from order.models import OrderProduct, Order



# Create your views here.



def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def account(request):
    url = request.META.get('HTTP_REFERER')
    
    current_user = request.user
   
    orders = Order.objects.filter(
        user_id=current_user.id, ordered=True).order_by('-id')
    order_product = OrderProduct.objects.filter(
        user_id=current_user.id).order_by('-id')


    context = {
     
        
        'orders': orders,
      

        'order_product': order_product
    }

    return render(request, 'home/account.html', context)



@login_required(login_url='/login')
def user_orders(request):
    
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id).order_by('-id')
    context = {
               'orders': orders,
               }
    return render(request, 'home/user-orders.html', context)


@login_required(login_url='/login')
def user_orderdetail(request, id):
   
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)

    context = {
        
        'order': order,
        'orderitems': orderitems,
       
    }
    return render(request, 'home/user-order-details.html', context)


