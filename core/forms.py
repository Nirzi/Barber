from django import forms
from .models import Review, Master, Order


class OrderSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Поиск')
    by_name = forms.BooleanField(required=False, initial=True, label='По имени клиента')
    by_phone = forms.BooleanField(required=False, label='По телефону')
    by_comment = forms.BooleanField(required=False, label='По комментарию')
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['client_name', 'text', 'rating', 'master', 'photo']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'master': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'client_name': 'Имя клиента',
            'text': 'Отзыв',
            'master': 'Мастер',
            'photo': 'Фотография',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['master'].queryset = Master.objects.filter(is_active=True)
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client_name', 'phone', 'appointment_date', 'comment', 'services']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'services': forms.CheckboxSelectMultiple()
        }