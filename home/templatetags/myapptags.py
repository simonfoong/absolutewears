from django import template
from django.urls import reverse

from home.models import Setting

from store.models import ShopCart, Category

register = template.Library()


@register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count

@register.simple_tag
def settingstag():
    setting = Setting.objects.get(pk=1)
    return setting


@register.simple_tag
def shopcarttag(userid):
    shopcart = ShopCart.objects.filter(user_id=userid)
    return shopcart

@register.simple_tag
def totaltag(userid):
    total = 0
    shopcart = ShopCart.objects.filter(user_id=userid)
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity
    return total
    

@register.simple_tag
def categorylist():
    return Category.objects.all()
