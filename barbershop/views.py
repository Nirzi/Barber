from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from core.models import Master, Service, Order, Review
from core.forms import OrderSearchForm
from django.shortcuts import render
from django import forms
from django.shortcuts import redirect
from django.utils.timezone import now



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
    latest_orders = Order.objects.filter(appointment_date__gte=now()).order_by("appointment_date")[:3]

    if request.method == "POST":
        client_name = request.POST.get("client_name")
        phone = request.POST.get("phone")
        appointment_date = request.POST.get("appointment_date")
        comment = request.POST.get("comment")

        if client_name and phone and appointment_date:
            Order.objects.create(
                client_name=client_name,
                phone=phone,
                appointment_date=appointment_date,
                comment=comment
            )
            return redirect("orders_list")

    context = {
        "orders": orders,
        "form": form,
        "latest_orders": latest_orders,
    }
    return render(request, "core/orders_list.html", context)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {"order": order}
    return render(request, "core/order_detail.html", context)


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description", "price", "duration", "is_popular", "image"]


def service_create(request):
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("landing")
        else:
            return render(request, "core/service_create.html", {"form": form, "error_message": "Пожалуйста, исправьте ошибки в форме."})
    else:
        form = ServiceForm()
    return render(request, "core/service_create.html", {"form": form})

