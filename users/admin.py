from django.contrib import admin

from .models import Userprofile

# Register your models here.


class UserprofileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address', 'image_tag']

admin.site.register(Userprofile, UserprofileAdmin)