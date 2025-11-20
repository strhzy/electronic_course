from django import forms
from main.models import Order, OrderItem

class CartAddProductForm(forms.Form):
    count = forms.IntegerField(min_value=1, initial=1, label='Количество', widget=forms.NumberInput(attrs={'class':'form-control'}))
    reload=forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['comment', 'delivery_address']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'comment': 'Комментарий',
            'delivery_address': 'Адрес доставки',
        }