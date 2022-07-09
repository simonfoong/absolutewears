from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
# from django.forms import ModelForm
from django.forms import ModelForm, TextInput, Textarea
from django.db.models import Avg, Count
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
# from mptt.fields import TreeForeignKey
# from mptt.models import MPTTModel

from django.dispatch import receiver
from django.template.defaultfilters import slugify
# from django_countries.fields import CountryField
# from django_countries.widgets import CountrySelectWidget
# from taggit.managers import TaggableManager


# class Category(MPTTModel):
#     parent = TreeForeignKey(
#         'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     slug = models.SlugField(null=False, unique=True)

#     def __str__(self):
#         return self.title

#     class MPTTMeta:
#         order_insertion_by = ['title']

#     def get_absolute_url(self):
#         return reverse('category_products', kwargs={'id': self.id, 'slug': self.slug})

#     def __str__(self):                           # __str__ method elaborated later in
#         # post.  use __unicode__ in place of
#         full_path = [self.title]
#         k = self.parent
#         while k is not None:
#             full_path.append(k.title)
#             k = k.parent
#         return ' / '.join(full_path[::-1])


class Category(models.Model):
    SPEC = (
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Children', 'Children'),
    )
    spec = models.CharField(max_length=10, choices=SPEC, default='Men')
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return f'{self.spec} - {self.title}'

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)

        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )


    
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )

    # many to one relation with Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    title = models.CharField(max_length=150)
    
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='store/images/')
    price = models.IntegerField()
    discount_price = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True)
    amount = models.IntegerField(
        default=1, help_text='how many do you have in stock')
    minamount = models.IntegerField(
        default=1, help_text='Minimum left to be sold')
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
   
    slug = models.SlugField(null=False, unique=True,
                            help_text='DO NOT CHANGE THIS AT ALL!!')
    # status = models.CharField(max_length=10, choices=STATUS)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'image'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'id': self.id, 'slug': self.slug})

    def averagereview(self):
        reviews = Comment.objects.filter(
            product=self).aggregate(average=Avg('rate'))
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews["average"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(
            product=self).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    def image2(self):
        i = Images.objects.filter(product_id=self.id).last()
        return i.image.url


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='app/product/images/')

    def __str__(self):
        return f'{self.product.title}-images'


class Comment(models.Model):
    # STATUS = (
    #     ('New', 'New'),
    #     ('True', 'True'),
    #     ('False', 'False'),
    # )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    # status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']


class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, blank=True, null=True)
    image_id = models.IntegerField(blank=True, null=True, default=0)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    variant = models.ForeignKey(
        Variants, on_delete=models.SET_NULL, blank=True, null=True)
    # ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return (self.product.price)

    @property
    def amount(self):
        return (self.quantity * self.product.price)

    @property
    def varamount(self):
        return (self.quantity * self.variant.price)


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']
