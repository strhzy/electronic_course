from django.contrib import admin
from django.urls import path

from .views import home,catalog,about,CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,ManufacturerListView, ManufacturerDetailView, ManufacturerCreateView, ManufacturerUpdateView, ManufacturerDeleteView,    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,     CustomerListView, CustomerDetailView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView,    ReviewListView, ReviewDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView,    OrderListView, OrderDetailView, OrderCreateView, OrderUpdateView, OrderDeleteView,    OrderItemListView, OrderItemDetailView, OrderItemCreateView, OrderItemUpdateView, OrderItemDeleteView, CartItemListView, CartItemDetailView, CartItemCreateView, CartItemUpdateView, CartItemDeleteView, login_user, registration_user, logout_user, profile_page

urlpatterns = [
    path('', home, name='home'),
    path('catalog/', catalog, name='catalog'),
    path('<int:product_id>/', about, name='about'),
    path('profile/',profile_page, name="profile_page"),

    path('login/', login_user, name='login_page'),
    path('registration/', registration_user, name='registration_page'),
    path('logout/', logout_user, name='logout_page'),

    path('categories/', CategoryListView, name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView, name='category_detail'),
    path('categories/create/', CategoryCreateView, name='category_create'),
    path('categories/<int:pk>/update/', CategoryUpdateView, name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView, name='category_delete'),

    path('manufacturers/', ManufacturerListView, name='manufacturer_list'),
    path('manufacturers/<int:pk>/', ManufacturerDetailView, name='manufacturer_detail'),
    path('manufacturers/create/', ManufacturerCreateView, name='manufacturer_create'),
    path('manufacturers/<int:pk>/update/', ManufacturerUpdateView, name='manufacturer_update'),
    path('manufacturers/<int:pk>/delete/', ManufacturerDeleteView, name='manufacturer_delete'),

    path('products/', ProductListView, name='product_list'),
    path('products/<int:pk>/', ProductDetailView, name='product_detail'),
    path('products/create/', ProductCreateView, name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView, name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView, name='product_delete'),

    path('customers/', CustomerListView, name='customer_list'),
    path('customers/<int:pk>/', CustomerDetailView, name='customer_detail'),
    path('customers/create/', CustomerCreateView, name='customer_create'),
    path('customers/<int:pk>/update/', CustomerUpdateView, name='customer_update'),
    path('customers/<int:pk>/delete/', CustomerDeleteView, name='customer_delete'),

    path('reviews/', ReviewListView, name='review_list'),
    path('reviews/<int:pk>/', ReviewDetailView, name='review_detail'),
    path('reviews/create/', ReviewCreateView, name='review_create'),
    path('reviews/<int:pk>/update/', ReviewUpdateView, name='review_update'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView, name='review_delete'),

    path('orders/', OrderListView, name='order_list'),
    path('orders/<int:pk>/', OrderDetailView, name='order_detail'),
    path('orders/create/', OrderCreateView, name='order_create'),
    path('orders/<int:pk>/update/', OrderUpdateView, name='order_update'),
    path('orders/<int:pk>/delete/', OrderDeleteView, name='order_delete'),

    path('orderitems/', OrderItemListView, name='orderitem_list'),
    path('orderitems/<int:pk>/', OrderItemDetailView, name='orderitem_detail'),
    path('orderitems/create/', OrderItemCreateView, name='orderitem_create'),
    path('orderitems/<int:pk>/update/', OrderItemUpdateView, name='orderitem_update'),
    path('orderitems/<int:pk>/delete/', OrderItemDeleteView, name='orderitem_delete'),

    path('cartitems/', CartItemListView, name='cartitem_list'),
    path('cartitems/<int:pk>/', CartItemDetailView, name='cartitem_detail'),
    path('cartitems/create/', CartItemCreateView, name='cartitem_create'),
    path('cartitems/<int:pk>/update/', CartItemUpdateView, name='cartitem_update'),
    path('cartitems/<int:pk>/delete/', CartItemDeleteView, name='cartitem_delete'),
]