from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
    
class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название производителя")
    country = models.CharField(max_length=100, blank=True, verbose_name="Страна")
    website = models.URLField(blank=True, verbose_name="Веб-сайт")

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название товара")
    description=models.TextField(max_length=1024, null=True, blank=True, default="Нет описания", verbose_name="Описание товара")
    price = models.FloatField(verbose_name="Цена")
    photo = models.ImageField(upload_to="products/")
    is_exists = models.BooleanField(default=True)

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, verbose_name="Производитель")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    address = models.TextField(blank=True, verbose_name="Адрес")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customers", verbose_name="Клиент", null=0)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name="Товар")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews", verbose_name="Клиент")
    rating = models.PositiveSmallIntegerField(verbose_name="Рейтинг (1-5)", choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата отзыва")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв на {self.product.name} от {self.customer}"
    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name="Клиент")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    delivery_address = models.CharField(max_length=150, verbose_name="Адрес доставки",default="")
    total_price = models.FloatField(verbose_name="Итог", default=0)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.id} от {self.buyer_firstname} {self.buyer_surname}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    @property
    def total(self):
        return self.quantity * self.product.price
    total.fget.short_description = "Общая цена"

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

class CartItem(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Покупатель")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
    
class Log(models.Model):

    created_at = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=True, verbose_name="Сообщение лога")
    table = models.TextField(blank=True, verbose_name="Таблица")

    class Meta:
        verbose_name = "Лог"

    def __str__(self):
        return f"{self.table}: {self.message} - {self.created_at}"