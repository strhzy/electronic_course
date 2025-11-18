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
# Category Views

@staff_member_required
class CategoryListView(ListView):
    model = Category
    template_name = 'forms/category/category_list.html'
    context_object_name = 'categories'

@staff_member_required
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'forms/category/category_detail.html'

@staff_member_required
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'forms/category/category_form.html'
    success_url = reverse_lazy('category_list')

@staff_member_required
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'forms/category/category_form.html'
    success_url = reverse_lazy('category_list')

@staff_member_required
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'forms/category/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

# Manufacturer Views

@staff_member_required
class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = 'forms/manufacturer/manufacturer_list.html'
    context_object_name = 'manufacturers'

@staff_member_required
class ManufacturerDetailView(DetailView):
    model = Manufacturer
    template_name = 'forms/manufacturer/manufacturer_detail.html'

@staff_member_required
class ManufacturerCreateView(CreateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'forms/manufacturer/manufacturer_form.html'
    success_url = reverse_lazy('manufacturer_list')

@staff_member_required
class ManufacturerUpdateView(UpdateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'forms/manufacturer/manufacturer_form.html'
    success_url = reverse_lazy('manufacturer_list')

@staff_member_required
class ManufacturerDeleteView(DeleteView):
    model = Manufacturer
    template_name = 'forms/manufacturer/manufacturer_confirm_delete.html'
    success_url = reverse_lazy('manufacturer_list')

# Product Views

@staff_member_required
class ProductListView(ListView):
    model = Product
    template_name = 'forms/product/product_list.html'
    context_object_name = 'products'

@staff_member_required
class ProductDetailView(DetailView):
    model = Product
    template_name = 'forms/product/product_detail.html'

@staff_member_required
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'forms/product/product_form.html'
    success_url = reverse_lazy('product_list')

@staff_member_required
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'forms/product/product_form.html'
    success_url = reverse_lazy('product_list')

@staff_member_required
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'forms/product/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

# Customer Views

@staff_member_required
class CustomerListView(ListView):
    model = Customer
    template_name = 'forms/customer/customer_list.html'
    context_object_name = 'customers'

@staff_member_required
class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'forms/customer/customer_detail.html'

@staff_member_required
class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'forms/customer/customer_form.html'
    success_url = reverse_lazy('customer_list')

@staff_member_required
class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'forms/customer/customer_form.html'
    success_url = reverse_lazy('customer_list')

@staff_member_required
class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'forms/customer/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')

# Review Views

@staff_member_required
class ReviewListView(ListView):
    model = Review
    template_name = 'forms/review/review_list.html'
    context_object_name = 'reviews'

@staff_member_required
class ReviewDetailView(DetailView):
    model = Review
    template_name = 'forms/review/review_detail.html'

@staff_member_required
class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'forms/review/review_form.html'
    success_url = reverse_lazy('review_list')

@staff_member_required
class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'forms/review/review_form.html'
    success_url = reverse_lazy('review_list')

@staff_member_required
class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'forms/review/review_confirm_delete.html'
    success_url = reverse_lazy('review_list')

# Order Views

@staff_member_required
class OrderListView(ListView):
    model = Order
    template_name = 'forms/order/order_list.html'
    context_object_name = 'orders'

@staff_member_required
class OrderDetailView(DetailView):
    model = Order
    template_name = 'forms/order/order_detail.html'

@staff_member_required
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'forms/order/order_form.html'
    success_url = reverse_lazy('order_list')

@staff_member_required
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'forms/order/order_form.html'
    success_url = reverse_lazy('order_list')

@staff_member_required
class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'forms/order/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')

# OrderItem Views

@staff_member_required
class OrderItemListView(ListView):
    model = OrderItem
    template_name = 'forms/orderitem/orderitem_list.html'
    context_object_name = 'order_items'

@staff_member_required
class OrderItemDetailView(DetailView):
    model = OrderItem
    template_name = 'forms/orderitem/orderitem_detail.html'

@staff_member_required
class OrderItemCreateView(CreateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = 'forms/orderitem/orderitem_form.html'
    success_url = reverse_lazy('orderitem_list')

@staff_member_required
class OrderItemUpdateView(UpdateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = 'forms/orderitem/orderitem_form.html'
    success_url = reverse_lazy('orderitem_list')

@staff_member_required
class OrderItemDeleteView(DeleteView):
    model = OrderItem
    template_name = 'forms/orderitem/orderitem_confirm_delete.html'
    success_url = reverse_lazy('orderitem_list')

# CartItem Views

@staff_member_required
class CartItemListView(ListView):
    model = CartItem
    template_name = 'forms/cartitem/cartitem_list.html'
    context_object_name = 'cart_items'

@staff_member_required
class CartItemDetailView(DetailView):
    model = CartItem
    template_name = 'forms/cartitem/cartitem_detail.html'

@staff_member_required
class CartItemCreateView(CreateView):
    model = CartItem
    form_class = CartItemForm
    template_name = 'forms/cartitem/cartitem_form.html'
    success_url = reverse_lazy('cartitem_list')

@staff_member_required
class CartItemUpdateView(UpdateView):
    model = CartItem
    form_class = CartItemForm
    template_name = 'forms/cartitem/cartitem_form.html'
    success_url = reverse_lazy('cartitem_list')

@staff_member_required
class CartItemDeleteView(DeleteView):
    model = CartItem
    template_name = 'forms/cartitem/cartitem_confirm_delete.html'
    success_url = reverse_lazy('cartitem_list')

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