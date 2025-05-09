from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from core.models import Master, Service, Order, Review
from core.forms import OrderSearchForm
from django.shortcuts import render
from django import forms
from django.shortcuts import redirect
from django.utils.timezone import now
from django.http import JsonResponse
from core.forms import ReviewForm
from django.core.paginator import Paginator






def landing(request):
    masters = Master.objects.filter(is_active=True)
    services = Service.objects.all()

    rating = request.GET.get("rating")
    reviews_qs = Review.objects.filter(is_published=True).order_by("-created_at")
    if rating:
        reviews_qs = reviews_qs.filter(rating=rating)

    paginator = Paginator(reviews_qs, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "masters": masters,
        "services": services,
        "page_obj": page_obj,  # <- это обязательно
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
  
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.is_published = True
            review.save()
            return redirect('thanks')
    else:
        form = ReviewForm()
    return render(request, 'core/review_form.html', {'form': form})



def get_master_info(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        master_id = request.GET.get('master_id')
        try:
            master = Master.objects.get(id=master_id)
            data = {
                'id': master.id,
                'name': master.name,
                'experience': master.experience,
                'photo': master.photo.url if master.photo else None,
                'services': list(master.services.values('id', 'name', 'price')),
            }
            return JsonResponse({'success': True, 'master': data})
        except Master.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Мастер не найден'})
    return JsonResponse({'success': False, 'error': 'Некорректный запрос'})

