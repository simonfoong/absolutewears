from django.urls import path, include
from django.views.decorators.cache import cache_page
from home import views

urlpatterns = [
    # path('', views.Index.as_view(), name='home'),
    path('', views.IndexView.as_view(), name='home'),
    path('modal/', views.modal, name='modal'),

    path('contact-us/', views.contact, name='contact'),
    path('about-us/', views.about, name='about'),
    path('search-items/', views.search, name='search'),
    path('search_auto/', views.search_auto, name='search_auto'),
    # path('our-gallery/', views.GalleryView.as_view(), name='gallery'),
    # path('frequently-asked-questions/', views.FaqView.as_view(), name='faqs'),
]