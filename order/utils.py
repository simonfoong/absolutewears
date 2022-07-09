from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from store.models import ShopCart


def shopcart_only(view_func):
    def wrap(request, *args, **kwargs):
        if ShopCart.objects.filter(user_id=request.user.id):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('menu')
    return wrap