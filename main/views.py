from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, Manufacturer, Product, Customer, Review, Order, OrderItem, CartItem
from .forms import CategoryForm, ManufacturerForm, ProductForm, CustomerForm, ReviewForm, OrderForm, OrderItemForm, CartItemForm, RegistrationForm, LoginForm
from cart.forms import CartAddProductForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def cart(request):
    return render(request, 'main/cart.html')

def catalog(request):
    products = Product.objects.filter(is_exists=True)

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    manufacturer_id = request.GET.get('manufacturer')
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)

    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query) | products.filter(description__icontains=search_query)

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'manufacturers': manufacturers,
        'sort': sort or '',
        'category': category_id or '',
        'manufacturer': manufacturer_id or '',
        'search': search_query or '',
        'form_cart':CartAddProductForm
    }
    return render(request, 'main/catalog.html', context)

def about(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Чтобы оставить отзыв, войдите в аккаунт.")
            return redirect('login')  # или вернись обратно на страницу товара

        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Предотвращаем дублирующий отзыв
        if Review.objects.filter(product=product, customer=request.user).exists():
            messages.warning(request, "Вы уже оставили отзыв.")
            return redirect('about', product_id=product_id)

        try:
            rating = int(rating)
        except (ValueError, TypeError):
            messages.error(request, "Оценка должна быть числом.")
            return redirect('about', product_id=product_id)

        Review.objects.create(
            product=product,
            customer=request.user,
            rating=rating,
            comment=comment
        )
        messages.success(request, "Отзыв добавлен!")
        return redirect('about', product_id=product_id)

    # Отображение отзывов и товара
    reviews = Review.objects.filter(product=product).select_related('user')
    return render(request, 'main/about.html', {
        'product': product,
        'reviews': reviews
    })

def profile_page(request):
    orders = Order.objects.filter(user=request.user).order_by('id')    
    orders_with_items = []
    for order in orders:
        items = OrderItem.objects.filter(order=order)
        orders_with_items.append({
            'order': order,
            'items': items
        })

    context = {
        'orders_with_items': orders_with_items
    }
    
    return render(request, 'main/profile.html', context)

def login_user(request):
    if request.method=="POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('/')
    else:
        form=LoginForm()
    context = {
        'form':form
    }
    return render(request, 'auth/login.html', context)

def registration_user(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()  # ← создаём нового пользователя
            login(request, user)  # ← и сразу логиним его
            next_url = request.GET.get('next')
            return redirect(next_url or '/')
    else:
        form = RegistrationForm()
    
    context = {
        'form': form
    }
    return render(request, 'auth/registration.html', context)

def logout_user(request):
    logout(request)
    return redirect('/')