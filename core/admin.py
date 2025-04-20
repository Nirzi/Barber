from django.contrib import admin
from .models import Master, Service, Order, Review

admin.site.register(Master)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Review)
