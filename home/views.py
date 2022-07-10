from django.shortcuts import render
from django.views.generic import View, ListView
import json
from django.http import HttpResponse
from home.forms import SearchForm
from home.models import ContactMessage, ContactForm, Gallery, Faqs
from django.http import HttpResponseRedirect
from django.contrib import messages
from store.models import Product, Images, Category

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
        # sneakers = []
        sneakers = Product.objects.filter(category__title='Sneakers').order_by('?')[:20]
        # print(sneaks)
        # for rs in sneaks:
        #     if rs.variant == 'None':
        #         sneakers.append(rs)
        
        context.update({'title': 'homepage',
                    'featured': featured,
                    'sneakers': sneakers,
                        })
        print(sneakers)
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
                request, "Message sent. We will contact you shortly. Thank You")
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
        # 'title': "Contact Igwe's Palace",

        
        'form': form,
       
    }

    return render(request, 'home/contact.html', context)





def about(request):
    

    context = {
        'title': "Igwe's Palace",
       
    }

    return render(request, 'home/about.html', context)


def search(request):
    url = request.META.get('HTTP_REFERER')
    random_items = Product.objects.all().order_by('?')[:20]
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)

            
            context = {
                'products': products,
                'query':query,
                'random_items': random_items
            }
            return render(request, 'home/search-products.html', context)
    context = {
                
                'random_items': random_items
            }

    return render(request, 'home/search-products.html', context)


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title +" > " + rs.category.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)



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
