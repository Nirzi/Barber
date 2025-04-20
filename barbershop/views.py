from django.shortcuts import render, get_object_or_404
from core.models import Master, Service, Order, Review


def landing(request):
    masters = Master.objects.filter(is_active=True)
    services = Service.objects.all()
    reviews = Review.objects.filter(is_published=True)
    context = {"masters": masters, "services": services, "reviews": reviews}
    return render(request, "core/landing.html", context)

def thanks(request):
    return render(request, "core/thanks.html")

def orders_list(request):
    orders = Order.objects.all()
    context = {"orders": orders}
    return render(request, "core/orders_list.html", context)

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {"order": order}
    return render(request, "core/order_detail.html", context)
