from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from core.models import Master, Service, Order, Review


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


@login_required
def orders_list(request):
    search_query = request.GET.get("q", "")
    search_name = request.GET.get("search_name", "on")
    search_phone = request.GET.get("search_phone", "")
    search_comment = request.GET.get("search_comment", "")

    filters = Q()
    if search_query:
        if search_name:
            filters |= Q(client_name__icontains=search_query)
        if search_phone:
            filters |= Q(phone__icontains=search_query)
        if search_comment:
            filters |= Q(comment__icontains=search_query)

    orders = Order.objects.filter(filters).order_by("-date_created")
    context = {
        "orders": orders,
        "search_query": search_query,
        "search_name": search_name,
        "search_phone": search_phone,
        "search_comment": search_comment,
    }
    return render(request, "core/orders_list.html", context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {"order": order}
    return render(request, "core/order_detail.html", context)
