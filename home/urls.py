from django.urls import path, include
from django.views.decorators.cache import cache_page
from home import views

urlpatterns = [
    # path('', views.Index.as_view(), name='home'),
    path('', views.IndexView.as_view(), name='home'),
    path('modal/', views.modal, name='modal'),
    # path('our-menu/', views.menu, name='menu'),
    # path('events-center/', views.events, name='events'),
    # path('contact-us/', views.contact, name='contact'),
    # path('about-us/', views.about, name='about'),
    # path('our-gallery/', views.GalleryView.as_view(), name='gallery'),
    # path('frequently-asked-questions/', views.FaqView.as_view(), name='faqs'),
]