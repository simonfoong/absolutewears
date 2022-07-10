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
# from django_countries.fields import CountryField
# from django_countries.widgets import CountrySelectWidget
# from taggit.managers import TaggableManager



class Setting(models.Model):
    
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True, max_length=255)
    phone = models.CharField(blank=True, max_length=16)
    phone2 = models.CharField(blank=True, null=True, max_length=16)
    email = models.CharField(blank=True, max_length=50)
    logo = models.ImageField(blank=True, null=True, upload_to='images/logo')
    logofav = models.ImageField(blank=True, null=True, upload_to='images/logo')
    about_us = models.TextField(blank=True, null=True, max_length=255)
    delivery_fee = models.IntegerField()
    facebook = models.CharField(blank=True, max_length=150)
    instagram = models.CharField(blank=True, max_length=150)
    twitter = models.CharField(blank=True, max_length=150)
    youtube_video_id = models.CharField(blank=True, max_length=250)
    aboutus = RichTextUploadingField(null=True, blank=True)
    
    
    privacypolicy = RichTextUploadingField(null=True, blank=True)
    tandc = RichTextUploadingField(null=True, blank=True)
   

    def __str__(self):
        return self.title


class ContactMessage(models.Model):

   
    name = models.CharField(blank=True, max_length=50)
    email = models.CharField(blank=True, null=True, max_length=50)
    phone = models.IntegerField(blank=True) 
    message = models.TextField(blank=True, max_length=255)
    ip = models.CharField(blank=True, max_length=100)
    # note = models.CharField(blank=True, max_length=100)
    # date = models.DateTimeField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['phone','name', 'email', 'message']
    


class Faqs(models.Model):

    question = models.CharField(max_length=200)
    answer = RichTextUploadingField()

    def __str__(self):
        return self.question





class Subscribe(models.Model):
    email = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.email


class SubscribeForm(ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']
        widgets = {

            'email': TextInput(attrs={'class': 'email-box', 'placeholder': 'Email Address'}),

        }



class Gallery(models.Model):
    CATEGORY = (
        ('Restaurant', 'Restaurant'),
        ('Events', 'Events'),
    )
    
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images/')
    category = models.CharField(max_length=20, choices=CATEGORY, default='Restaurant')
   
    def __str__(self):
        return self.title




