from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as u_login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import get_list_or_404, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.urls import reverse


from django.template.loader import render_to_string, get_template
# from .tokens import account_activation_token
import random
import json
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
import requests
from django.core import serializers
from .models import OrderProduct, Order
from home.models import Setting

from store.models import Product, ShopCart
from order.models import OrderProduct, Order, OrderForm
from users.models import Userprofile

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
# from xhtml2pdf import pisa

# from webpush import send_group_notification
from .utils import shopcart_only



# from weasyprint import HTML
# import tempfile
# from django.db.models import Sum




# Create your views here.


@login_required()
@shopcart_only
def checkout(request):
    url = request.META.get('HTTP_REFERER')
    # setting = Setting.objects.get(pk=1)
  
    # category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)

        if form.is_valid():

            data = Order()
            # payment_option = form.cleaned_data.get('payment_option')
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(length=8, allowed_chars='0123456789')  # random code
            data.code = ordercode
            
            # for rs in shopcart:
            #     data.product_id   = rs.product_id
            data.save()
            # data.product.set(shopcart)
            data.save()

            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()

            # return render(request, 'home/card-payment.html', {'orderid': data.id, 'total': total, 'title': 'Paystack Payment'})
            return HttpResponseRedirect(reverse('card', kwargs={'pk':data.id}))

        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(url)

    form = OrderForm()
    profile = Userprofile.objects.get(user_id=current_user.id)

    context = {'shopcart': shopcart,
               'title': 'Checkout',
            
               'total': total,
               'form': form,
               'profile': profile,
              
               }
    return render(request, 'home/checkout-partial.html', context)

def card(request, pk):
    order = Order.objects.get(pk=pk)
    context = {
        'order': order
    }
    return render(request, 'home/card-payment.html', context)

@login_required()
def paystack(request, pk):
    orderid = pk
    order = Order.objects.get(pk=orderid)
    fee = Setting.objects.get(pk=1)
    amount = int(order.total) + int(fee.delivery_fee)
    # print(order.total)
    url = 'https://api.paystack.co/transaction/initialize'
    headers = {
        'Authorization': 'Bearer sk_test_fbbe364ab31835ea5856bd2536619e7e70478fc8',
        'Content-Type': 'apllication/json',
        'Accept': 'application/json',
    }
    cash = {
        "email": request.user.email,
        "amount": amount*100
    }
    x = requests.post(url, data=json.dumps(cash), headers=headers)
    # print(x.status_code)
    results = x.json()
    # print('results: ', results)
    # link = []
    # print(x.json())
    # print(x['data']['authorization_url'])
    link = results['data']['authorization_url']
    order.ref_code = results['data']['reference']
    order.save()

    return HttpResponseRedirect(link)


def order_completed(request):
    if(request.GET.get('trxref') != None):
        trxref = request.GET.get('trxref')
        

        # print(trxref)

        paid = Order.objects.get(ref_code=trxref)
        
        paid.ordered = True
        paid.save()
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        for rs in shopcart:
            # paid.product_id   = rs.product_id
            # paid.save()
            product = Product.objects.get(id=rs.product_id)
            product.amount -= rs.quantity
            product.save()
           
        
        paid.product.set(shopcart)
        paid.save()
        
        # shopcart.save()
        # alert_group = User.objects.get(pk=1)
        # print(alert_group)
        # webpush = {"alert_group": 'alert_group' }
        # payload = {
        #     'head': 'New Order for Delivery', 
        #     'body': paid.address, 
        #     'icon': 'https://i.imgur.com/dRDxiCQ.png', 
        #     'url': 'http://localhost:8000/'
        #     }

        # send_group_notification(group_name='alert_group', payload=payload, ttl=1000)


       


    context = {
        'title': 'Order Completed - The Monkey Post',
        'paid': paid
        # 'webpush': webpush

       

    }

    return render(request, 'home/order-completed.html', context)



# def render_pdf_view(request, *args, **kwargs):
#     pk = kwargs.get('pk')
#     receipt = get_object_or_404(Order, pk=pk)
#     orderitems = OrderProduct.get_object_or_404(Order, pk=id)
#     setting = get_object_or_404(Setting, pk=1)
#     template_path = 'home/pdf.html'
#     context = {'receipt': receipt,
#                 'setting': setting,
#                 'orderitems': orderitems
#         }
  
#     response = HttpResponse(content_type='application/pdf')


  
    
#     response['Content-Disposition'] = 'inline; filename="report.pdf"'
#     response['content-Transfer-Encoding'] = 'binary'
#     html_string = render_to_string('home/pdf.html', context)
#     html = HTML(string=html_string)

#     result = html.write_pdf()

#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name, 'rb')
#         response.write(output.read())

#     return response



    # template = get_template(template_path)
    # html = template.render(context)

 
    # pisa_status = pisa.CreatePDF(
    #    html, dest=response)
  
    # if pisa_status.err:
    #    return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response


def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/9.6.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/9.6.6/firebase-analytics.js"); ' \
         'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyAlSmjZuZ9NVXWZVeKGWnN6cuTWI4Gkw1M",' \
         '        authDomain: "igwespalace-notif.firebaseapp.com",' \
         '        projectId: "igwespalace-notif",' \
         '        storageBucket: "igwespalace-notif.appspot.com",' \
         '        messagingSenderId: "727967837003",' \
         '        appId: "1:727967837003:web:93db85f2de8912757856ce",' \
         '        measurementId: "G-E1MJJ7SXGK"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")


def testview(request):
    return render(request, 'home/test.html')