from django import forms
from .models import Category, Manufacturer, Product, Customer, Review, Order, OrderItem, CartItem
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': "Название категории",
            'description': "Описание категории"
        }

class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name', 'country', 'website']
        widgets = {
            'website': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
        }
        labels = {
            'name': "Название производителя",
            'country': "Страна",
            'website': "Веб-сайт"
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'photo', 'is_exists', 'manufacturer', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'photo': forms.FileInput(),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'name': "Название товара",
            'description': "Описание товара",
            'price': "Цена",
            'photo': "Фотография",
            'is_exists': "В наличии",
            'manufacturer': "Производитель",
            'category': "Категория"
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4}),
            'email': forms.EmailInput(),
        }
        labels = {
            'first_name': "Имя",
            'last_name': "Фамилия",
            'email': "Email",
            'phone': "Телефон",
            'address': "Адрес"
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'customer', 'rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
        }
        labels = {
            'product': "Товар",
            'customer': "Клиент",
            'rating': "Рейтинг (1-5)",
            'comment': "Комментарий"
        }


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


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }
        labels = {
            'order': "Заказ",
            'product': "Товар",
            'quantity': "Количество",
        }


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['user', 'product', 'quantity', 'price']
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }
        labels = {
            'user': "Покупатель",
            'product': "Товар",
            'quantity': "Количество",
            'price': "Цена за единицу"
        }

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class':'form-control'}),
        min_length=2,
    )
    email = forms.CharField(
        label='E-Mail',
        widget=forms.EmailInput(attrs={'class':'form-control'})
    )
    password1 = forms.CharField(
        label='Придумайте пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

    class Meta:
        model = User
        fields=['username','email','password1','password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class':'form-control'}),
        min_length=2,
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )