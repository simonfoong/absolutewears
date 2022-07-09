from django.shortcuts import render
from django.views.generic import View, ListView

from home.models import ContactMessage, ContactForm, Gallery, Faqs
from django.http import HttpResponseRedirect
from django.contrib import messages
from store.models import Product, Images

# Create your views here.
class IndexView(ListView):
    model = Product
    template_name = 'home/index.html'
    context_object_name = 'products'
    ordering = ['-id']

    paginate_by = 20

    # def get_queryset(self):
    #     return Blog.objects.filter(tags__slug=self.kwargs.get('slug'))
    # def get_template_names(self):
    #     if self.request.htmx:
    #         return 'home/modal.html'
    #     return 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured = Product.objects.all().order_by('?')[:20]
        
        context.update({'title': 'homepage',
                    'featured': featured
                        })
        return context



def modal(request):
    id = request.GET.get('id')
    
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)


    return render(request, 'home/modal.html', {'product': product, 'images': images})



def contact(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data1 = form.cleaned_data
            data = ContactMessage()  # create relation with model
           
            data.name = form.cleaned_data['name']  # get form input data
            data.phone = form.cleaned_data['phone']  # get form input data
            data.email = form.cleaned_data['email']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(
                request, "Message sent. Igwe's Palace will contact you shortly. Thank You")
            # template = render_to_string('booking_template.html', {
            #                             'name': data1['name'],
            #                             'phone': data1['phone'],
            #                             'email': data1['email'],
            #                             'subject': data1['subject'],
            #                             'description': data1['description'],
            #                             'date': data1['date'], })

            # email = EmailMessage(
            #     'You have a new Booking! ',
            #     template,
            #     settings.EMAIL_HOST_USER,
            #     ['ceasarplusplus@gmail.com']

            # )


            # email.fail_silently = False
            # email.send()

            return HttpResponseRedirect(url)
    
    form = ContactForm()
   
    context = {
        'title': "Contact Igwe's Palace",

        
        'form': form,
       
    }

    return render(request, 'home/contact.html', context)


def events(request):
    images = Gallery.objects.filter(category='Events')[:12]
    

    context = {
        'title': 'Events',
        'images': images
       
    }

    return render(request, 'home/events.html', context)


def about(request):
    

    context = {
        'title': "Igwe's Palace",
       
    }

    return render(request, 'home/about.html', context)


class GalleryView(ListView):
    model = Gallery
    template_name = 'home/gallery.html'
    context_object_name = 'gallery'
    ordering = ['-id']
    # paginate_by = 25

class FaqView(ListView):
    model = Faqs
    template_name = 'home/faq.html'
    context_object_name = 'faqs'
    ordering = ['-id']
    # paginate_by = 25





def handler400(request, exception):
    return render(request, 'home/400.html', status=400)

def handler403(request, exception):
    return render(request, 'home/403.html', status=400)


def handler404(request, exception):
    return render(request, 'home/404.html', status=400)


def handler500(request):
    return render(request, 'home/500.html', status=400)
