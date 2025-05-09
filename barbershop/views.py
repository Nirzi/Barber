from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from core.models import Master, Service, Order, Review
from core.forms import OrderSearchForm


def landing(request):
    masters = Master.objects.filter(is_active=True)
    services = Service.objects.all()
    reviews = Review.objects.filter(is_published=True)
    context = {
        "masters": masters,
        "services": services,
        "reviews": reviews,
    }
    return render(request, "core/landing.html", context)


def thanks(request):
    return render(request, "core/thanks.html")


def orders_list(request):
    form = OrderSearchForm(request.GET or None)
    filters = Q()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            if form.cleaned_data.get('by_name'):
                filters |= Q(client_name__icontains=query)
            if form.cleaned_data.get('by_phone'):
                filters |= Q(phone__icontains=query)
            if form.cleaned_data.get('by_comment'):
                filters |= Q(comment__icontains=query)

    orders = Order.objects.filter(filters).order_by("-date_created")
    context = {
        "orders": orders,
        "form": form,
    }
    return render(request, "core/orders_list.html", context)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {"order": order}
    return render(request, "core/order_detail.html", context)
