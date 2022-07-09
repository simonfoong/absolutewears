
from django.urls import path, include
from django.views.decorators.cache import cache_page
from order import views
from django.views.generic import TemplateView

urlpatterns = [
    # path('', views.Index.as_view(), name='home'),
    path('checkout/', views.checkout, name='checkout'),
    path('testview/', views.testview, name='testview'),
    path('payment/paystack/<pk>', views.paystack, name='paystack'),
    path('order-completed/', views.order_completed, name='order_completed'),
    # path('/generatepdf/<pk>', views.render_pdf_view, name='generatepdf'),
    # path('firebase-messaging-sw.js', views.showFirebaseJS, name="show_firebase_js"),
    # path("firebase-messaging-sw.js",
    #     TemplateView.as_view(
    #         template_name="home/firebase-messaging-sw.js",
    #         content_type="application/javascript",
    #     ),
    #     name="firebase-messaging-sw.js"
    # ),
]