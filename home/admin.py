from django.contrib import admin
import admin_thumbnails
from mptt.admin import DraggableMPTTAdmin
from .models import Setting, Gallery, Faqs, ContactMessage




admin.site.register(ContactMessage)
admin.site.register(Setting)
admin.site.register(Gallery)
admin.site.register(Faqs)