from django.contrib import admin
from django.urls import path, include

from .views import (
    LandingPageView, ThanksView,
    OrdersListView, OrderCreateView, OrderDetailView,
    MasterDetailView, ServicesListView,
    ServiceCreateView, ServiceUpdateView,
    ReviewCreateView, MastersServicesAjaxView,
    MasterInfoAjaxView,
)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('users.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),

    path('', LandingPageView.as_view(), name='landing'),
    path('thanks/<str:source>/', ThanksView.as_view(), name='thanks'),

    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),

    path('masters/<int:pk>/', MasterDetailView.as_view(), name='master_detail'),

    path('services/', ServicesListView.as_view(), name='services_list'),
    path('services/create/', ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/update/', ServiceUpdateView.as_view(), name='service_update'),

    path('reviews/create/', ReviewCreateView.as_view(), name='create_review'),

    path('api/master-services/', MastersServicesAjaxView.as_view(), name='get_master_services'),
    path('api/master-info/', MasterInfoAjaxView.as_view(), name='get_master_info'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)