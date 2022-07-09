
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.contrib.auth.models import User

from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
import random
import json
from django.utils.crypto import get_random_string

from django.conf import settings
from django.core.mail import send_mail, EmailMessage
import requests
from .models import Category, Variants, Product, Images, ShopCart, ShopCartForm, Comment, CommentForm



class StoreView(ListView):
    model = Product
    template_name = 'store/store.html'
    context_object_name = 'products'
    ordering = ['-id']
    paginate_by = 28

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
       
        category = Category.objects.all()
       
        context.update({
            # 'title': 'Store | Top Quality Sports Wears and Accessories - The Monkey Post',    
                        'category': category,              
                        
                        })
        return context



def category_products(request, id, slug):
    
    category = Category.objects.all()
    
    # .order_by('id')[offset:limit]
    products = Product.objects.filter(category_id=id)

    
    catid = Product.objects.filter(category_id=id)[0]

    context = {

        'products': products,
        'shopcart': shopcart,
        'catid': catid,
        
        'category': category,
       
        # 'total_list': total_list,
        # 'list_set': list_set,
        # 'page': page,

        'title': 'Category Items - Monkey Post',
        # 'pagination': pagination
        # 'page_obj': page_obj,
    }
    return render(request, 'store/shop_category.html', context)

class StoreCategoryView(ListView):
    model = Product
    template_name = 'store/store_category.html'
    context_object_name = 'products'
    ordering = ['-id']
    paginate_by = 28
    

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        # category = Category.objects.all()
       
        context.update({'title': 'News Category - The Monkey Post', 
                        # 'category': category,                     
                        # 'top_trends': top_trends,                                       
                        })
        return context

# @login_required(login_url='/login')  # Check login
# def addtoshopcart(request, id):
#     url = request.META.get('HTTP_REFERER')  # get last url
#     current_user = request.user  # Access User Session information
#     product = Product.objects.get(pk=id)

#     checkinproduct = ShopCart.objects.filter(
#         product_id=id, user_id=current_user.id)  # Check product in shopcart
#     if checkinproduct:
#         control = 1  # The product is in the cart
#     else:
#         control = 0  # The product is not in the cart"""

#     if request.method == 'POST':  # if there is a post
#         form = ShopCartForm(request.POST)
#         if form.is_valid():
#             if control == 1:
#                 # Update  shopcart

#                 data = ShopCart.objects.get(
#                     product_id=id, user_id=current_user.id)

#                 data.quantity += form.cleaned_data['quantity']
#                 data.save()  # save data
#             else:  # Inser to Shopcart
#                 data = ShopCart()
#                 data.user_id = current_user.id
#                 data.product_id = id
#                 data.quantity = form.cleaned_data['quantity']
#                 data.save()
#         messages.success(request, "Product added to Shopcart ")
#         return HttpResponseRedirect(url)

#     else:  # if there is no post
#         if control == 1:
#             # Update  shopcart
#             data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
#             data.quantity += 1
#             data.save()  #
#         else:  # Inser to Shopcart
#             data = ShopCart()
#             data.user_id = current_user.id
#             data.product_id = id
#             data.quantity = 1
#             data.save()  #
#         messages.success(request, "Product added to Shopcart")
#         return HttpResponseRedirect(url)


@login_required(login_url='/login')
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product = Product.objects.get(pk=id)
    variantid = request.POST.get('variantid')

    if product.variant != 'None':
        variantid = request.POST.get('variantid')  # from variant add to cart
        checkinvariant = ShopCart.objects.filter(
            variant_id=variantid, user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""
    else:
        checkinproduct = ShopCart.objects.filter(
            product_id=id, user_id=current_user.id)  # Check product in shopcart
        if checkinproduct:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                if product.variant == 'None':
                    data = ShopCart.objects.get(
                        product_id=id, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(
                        product_id=id, variant_id=variantid, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
                messages.info(request, "Product added to Shopcart ")
                return HttpResponseRedirect(url)  # save data
            else:  # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
                messages.info(request, "Product added to Shopcart ")
                return HttpResponseRedirect(url)

        else:
            messages.error(request, "invalid ")
            return HttpResponseRedirect(url)

    else:  # if there is no post
        if control == 1:
            # Update  shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  # Inser to Shopcart
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id = None
            data.save()  #
        messages.info(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)





def product_detail(request, id, slug):
   
    category = Category.objects.all()
    query = request.GET.get('q')
    
    product = Product.objects.get(pk=id)
    pkk = product.category.id
    rel_products = Product.objects.filter(category_id=pkk)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id)
   

    context = {
        
        'product': product,
        'images': images,
        # 'title': 'Item Details - The Monkey Post Store',       
        'comments': comments,       
        'rel_products': rel_products,
        'category': category,

    }

    if product.variant != "None":  # Product with variants
        if request.method == 'POST':  # if we select color
            # selected product by click color radio
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)
            colors = Variants.objects.filter(
                product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw(
                'SELECT * FROM  store_variants  WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title+' Size:' + \
                str(variant.size) + ' Color:' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(
                product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw(
                'SELECT * FROM  store_variants  WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant, 'query': query
                        })

    return render(request, 'home/product-details.html', context)



# def ajaxcolor(request):
#     data = {}
#     if request.POST.get('action') == 'post':
#         size_id = request.POST.get('size')
#         productid = request.POST.get('productid')
#         colors = Variants.objects.filter(product_id=productid, size_id=size_id)
#         context = {
#             'size_id': size_id,
#             'productid': productid,
#             'colors': colors,
#         }
#         data = {'rendered_table': render_to_string(
#             'home/color_list.html', context=context)}
#         return JsonResponse(data)
#     return JsonResponse(data)

def ajaxcolor(request):
    data = {}
    # if request.POST.get('action') == 'post':
    size_id = request.POST.get('size')
    productid = request.POST.get('productid')
    colors = Variants.objects.filter(product_id=productid, size_id=size_id)
    context = {
        'size_id': size_id,
        'productid': productid,
        'colors': colors,
    }
    # data = {'rendered_table': render_to_string(
    #     'home/color_list.html', context=context)}
    # return JsonResponse(data)
    # return JsonResponse(data)
    return render(request, 'home/color_list.html', context)



def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    # return HttpResponse(url)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if Comment.objects.filter(product_id=id, user=request.user).exists():
                messages.warning(
                    request, "You have posted a review already!")
                return HttpResponseRedirect(url)
            else:

                data = Comment()
                data.subject = form.cleaned_data['subject']
                data.comment = form.cleaned_data['comment']
                data.rate = form.cleaned_data['rate']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = id
                current_user = request.user
                data.user_id = current_user.id
                data.save()
                messages.success(
                    request, "Your review has been sent. Thank you for your interest.")
                return HttpResponseRedirect(url)

        else:
            messages.error(
                request, form.errors)

            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)


@login_required(login_url='/login')  # Check login
def user_deletecomment(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.info(request, 'Comment deleted..')
    return HttpResponseRedirect(url)


def shopcart(request):
    category = Category.objects.all()
 
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0

    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity

    context = {
        'category': category,
        'shopcart': shopcart,
   

        'total': total,
     
        'title': 'Shopping Cart - The Monkey Post'

    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='/login')
def deletefromcart(request, id):
    url = request.META.get('HTTP_REFERER')
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Item removed from cart")
    return HttpResponseRedirect(url)



