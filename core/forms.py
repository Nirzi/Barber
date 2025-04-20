from django import forms

class OrderSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Поиск')
    by_name = forms.BooleanField(required=False, initial=True, label='По имени клиента')
    by_phone = forms.BooleanField(required=False, label='По телефону')
    by_comment = forms.BooleanField(required=False, label='По комментарию')