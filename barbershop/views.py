from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, View
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Q, F
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.models import Master, Service, Order, Review
from core.forms import OrderSearchForm, ReviewForm, OrderForm
from core.mixins import StaffRequiredMixin, LoginRequiredMixin

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name","description","price","duration","is_popular","image"]
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "description": forms.Textarea(attrs={"class":"form-control"}),
            "price": forms.NumberInput(attrs={"class":"form-control"}),
            "duration": forms.NumberInput(attrs={"class":"form-control"}),
            "is_popular": forms.CheckboxInput(attrs={"class":"form-check-input"}),
            "image": forms.ClearableFileInput(attrs={"class":"form-control"}),
        }

class LandingPageView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = "core/landing.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        masters = Master.objects.filter(is_active=True)
        services = Service.objects.all()
        rating = self.request.GET.get("rating")
        qs = Review.objects.filter(is_published=True).order_by("-created_at")
        if rating:
            qs = qs.filter(rating=rating)
        paginator = Paginator(qs, 3)
        ctx.update({
            "masters": masters,
            "services": services,
            "page_obj": paginator.get_page(self.request.GET.get("page")),
        })
        return ctx


class ThanksView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = "core/thanks.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        source = self.kwargs.get("source")
        ctx["message"] = {
            "order": "Спасибо за ваш заказ! Мы с вами свяжемся.",
            "review": "Спасибо за ваш отзыв!",
        }.get(source, "Спасибо!")
        return ctx

class OrdersListView(StaffRequiredMixin, ListView):
    model = Order
    template_name = "core/orders_list.html"
    context_object_name = "orders"
    def get_queryset(self):
        form = OrderSearchForm(self.request.GET or None)
        f = Q()
        if form.is_valid():
            q = form.cleaned_data["query"]
            if q:
                if form.cleaned_data["by_name"]:
                    f |= Q(client_name__icontains=q)
                if form.cleaned_data["by_phone"]:
                    f |= Q(phone__icontains=q)
                if form.cleaned_data["by_comment"]:
                    f |= Q(comment__icontains=q)
        return (Order.objects.filter(f)
                        .select_related("master")
                        .prefetch_related("services")
                        .order_by("-date_created"))
    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["form"] = OrderSearchForm(self.request.GET or None)
        ctx["latest_orders"] = (Order.objects
                                     .filter(appointment_date__gte=now())
                                     .order_by("appointment_date")[:3])
        return ctx
    def post(self, request, *args, **kwargs):
        name = request.POST.get("client_name")
        phone = request.POST.get("phone")
        date = request.POST.get("appointment_date")
        comment = request.POST.get("comment")
        try:
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except:
            date = None
        if name and phone and date:
            Order.objects.create(
                client_name=name,
                phone=phone,
                appointment_date=date,
                comment=comment,
            )
        return redirect("orders_list")

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "core/order_form.html"
    def get_success_url(self):
        return reverse_lazy("thanks", kwargs={"source":"order"})
    def form_valid(self, form):
        messages.success(self.request, "Заказ успешно создан.")
        return super().form_valid(form)

class OrderDetailView(StaffRequiredMixin, DetailView):
    model = Order
    template_name = "core/order_detail.html"
    pk_url_kwarg = "order_id"
    def dispatch(self, req, *a, **k):
        if not req.user.is_staff:
            messages.error(req, "У вас нет доступа.")
        return super().dispatch(req, *a, **k)

class MasterDetailView(DetailView):
    model = Master
    template_name = "core/master_detail.html"
    context_object_name = "master"
    def get_queryset(self):
        return Master.objects.filter(is_active=True).prefetch_related("services")
    def get_object(self, qs=None):
        obj = super().get_object(qs)
        if hasattr(obj, "view_count"):
            obj.view_count = F("view_count") + 1
            obj.save(update_fields=["view_count"])
        seen = self.request.session.get("viewed_masters", [])
        if obj.id not in seen:
            seen.append(obj.id)
            self.request.session["viewed_masters"] = seen
        return obj
    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["reviews"] = Review.objects.filter(master=self.object, is_published=True)
        ctx["title"] = f"Мастер: {self.object.name}"
        return ctx

class ServicesListView(StaffRequiredMixin, ListView):
    model = Service
    template_name = "core/services_list.html"
    context_object_name = "services"

class ServiceCreateView(StaffRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "core/service_create.html"
    success_url = reverse_lazy("services_list")
    def form_valid(self, form):
        messages.success(self.request, "Услуга успешно создана.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Исправьте ошибки.")
        return super().form_invalid(form)

class ServiceUpdateView(StaffRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "core/service_update.html"
    success_url = reverse_lazy("services_list")
    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["title"] = f"Редактирование услуги: {self.object.name}"
        return ctx
    def form_valid(self, form):
        messages.success(self.request, "Услуга обновлена.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Исправьте ошибки.")
        return super().form_invalid(form)

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "core/review_form.html"
    def get_success_url(self):
        return reverse_lazy("thanks", kwargs={"source":"review"})
    def form_valid(self, form):
        r = form.save(commit=False)
        r.is_published = True
        r.save()
        messages.success(self.request, "Отзыв отправлен на модерацию.")
        return super().form_valid(form)

class MastersServicesAjaxView(View):
    def get(self, request, *a, **k):
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return JsonResponse({"success": False, "error": "Некорректный запрос"})
        mid = request.GET.get("master_id")
        services = Service.objects.filter(masters__id=mid).values("id","name","price")
        return JsonResponse({"success": True, "services": list(services)})

class MasterInfoAjaxView(View):
    def get(self, request, *a, **k):
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return JsonResponse({"success": False, "error": "Некорректный запрос"})
        try:
            m = Master.objects.get(id=request.GET.get("master_id"))
        except Master.DoesNotExist:
            return JsonResponse({"success": False, "error": "Мастер не найден"})
        data = {
            "id": m.id,
            "name": m.name,
            "experience": m.experience,
            "photo": m.photo.url if m.photo else None,
            "services": list(m.services.values("id","name","price")),
        }
        return JsonResponse({"success": True, "master": data})
      
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Регистрация прошла успешно. Пожалуйста, войдите.')
        return super().form_valid(form)
