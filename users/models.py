from django.db import models
from django.contrib.auth.models import User

from django.utils.safestring import mark_safe
# from mptt.fields import TreeForeignKey
# from mptt.models import MPTTModel


from PIL import Image


class Userprofile(models.Model):
    # # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # # phone = models.IntegerField(blank=True, default=0)
    # email_confirmed = models.BooleanField(default=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(blank=True, default=0)
    address = models.CharField(max_length=150)
    # city = models.CharField(max_length=15)
    # state = models.CharField(max_length=10)
    image = models.ImageField(
        blank=True, upload_to='images/users/')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.username

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    # img = Image.open(self.image.path)

    # if img.height > 250 or img.width > 250:
    #     output_size = (250,250)
    #     img.thumbnail(output_size)
    #     img.save(image.path)



    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    
    image_tag.short_description = 'Image'