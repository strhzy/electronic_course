from django import forms
from main.models import Order, OrderItem

class CartAddProductForm(forms.Form):
    count = forms.IntegerField(min_value=1, initial=1, label='Количество', widget=forms.NumberInput(attrs={'class':'form-control'}))
    reload=forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['buyer_firstname', 'buyer_surname', 'comment', 'delivery_address']
        widgets = {
            'buyer_firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'buyer_surname': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'buyer_firstname': 'Имя покупателя',
            'buyer_surname': 'Фамилия покупателя',
            'comment': 'Комментарий',
            'delivery_address': 'Адрес доставки',
        }