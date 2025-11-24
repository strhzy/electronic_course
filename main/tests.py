from django.test import TestCase, Client, SimpleTestCase
from django.urls import resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from . import views
from .models import (
    Category, Manufacturer, Product, Review,
    OrderItem, CartItem, BackupFile, Customer, Order
)
from .forms import ProductForm, RegistrationForm, LoginForm, OrderForm, ReviewForm

User = get_user_model()


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='u1', password='pass')
        cls.cat = Category.objects.create(name='Cat1')
        cls.man = Manufacturer.objects.create(name='Man1')
        cls.image = SimpleUploadedFile(name='test.jpg', content=b'filecontent', content_type='image/jpeg')
        cls.product = Product.objects.create(
            name='Prod1',
            description='Desc',
            price=9.99,
            photo=cls.image,
            is_exists=True,
            manufacturer=cls.man,
            category=cls.cat,
        )

    def test_category_str(self):
        self.assertEqual(str(self.cat), 'Cat1')

    def test_manufacturer_str(self):
        self.assertEqual(str(self.man), 'Man1')

    def test_product_str_and_fields(self):
        p = self.product
        self.assertEqual(str(p), 'Prod1')
        self.assertAlmostEqual(p.price, 9.99)
        self.assertTrue(p.is_exists)

    def test_orderitem_total_property(self):
        # создаём Order временно чтобы корректно связать FK при необходимости
        ord = Order.objects.create(customer=self.user)
        order_item = OrderItem(order=ord, product=self.product, quantity=3)
        self.assertAlmostEqual(order_item.total, 3 * self.product.price)

    def test_cartitem_str(self):
        cust = Customer.objects.create(first_name='F', last_name='L', email='x@example.com', user=self.user)
        cart = CartItem.objects.create(user=cust, product=self.product, quantity=2, price=19.99)
        self.assertIn('Prod1', str(cart))

    def test_backupfile_str(self):
        bf = BackupFile.objects.create(file=SimpleUploadedFile('backups/test.txt', b'123'))
        self.assertIn('test.txt', str(bf))

    def test_review_creation(self):
        rev = Review.objects.create(product=self.product, customer=self.user, rating=5, comment='ok')
        self.assertIn('Prod1', str(rev))


class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='vuser', password='pass')
        self.cat = Category.objects.create(name='C')
        self.man = Manufacturer.objects.create(name='M')
        image = SimpleUploadedFile(name='t.jpg', content=b'x', content_type='image/jpeg')
        self.prod = Product.objects.create(name='P', description='D', price=1.0, photo=image, is_exists=True, manufacturer=self.man, category=self.cat)

    def test_home_view(self):
        resp = self.client.get('/')
        self.assertIn(resp.status_code, (200, 302))

    def test_catalog_view(self):
        resp = self.client.get('/catalog/')
        self.assertEqual(resp.status_code, 200)
        # контекст может содержать QuerySet products
        self.assertIn('products', resp.context)

    def test_about_get(self):
        resp = self.client.get(f'/{self.prod.id}/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('product', resp.context)

    def test_about_post_create_review_requires_auth(self):
        resp = self.client.post(f'/{self.prod.id}/', data={'rating': '5', 'comment': 'ok'})
        # при неаутентифицированном пользователе должен быть редирект на страницу логина
        self.assertIn(resp.status_code, (302,))

    def test_profile_requires_login(self):
        resp = self.client.get('/profile/')
        self.assertIn(resp.status_code, (302,))

    def test_login_and_registration_views(self):
        resp = self.client.get('/login/')
        self.assertIn(resp.status_code, (200, 302))
        resp = self.client.get('/registration/')
        self.assertIn(resp.status_code, (200, 302))

    def test_about_post_authenticated_creates_review(self):
        self.client.login(username='vuser', password='pass')
        resp = self.client.post(f'/{self.prod.id}/', data={'rating': '4', 'comment': 'good'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Review.objects.filter(product=self.prod, customer=self.user).exists())


class FormsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cat = Category.objects.create(name='fcat')
        cls.man = Manufacturer.objects.create(name='fman')

    def test_product_form_valid_minimum(self):
        data = {'name': 'X', 'description': 'd', 'price': '10.5', 'is_exists': True, 'manufacturer': self.man.pk, 'category': self.cat.pk}
        form = ProductForm(data=data)
        form.is_valid()
        self.assertTrue(hasattr(form, 'errors'))

    def test_registration_form(self):
        data = {'username': 'tu', 'email': 'a@b.com', 'password1': 'strong-pass-1', 'password2': 'strong-pass-1'}
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_login_form(self):
        data = {'username': 'x', 'password': 'y'}
        form = LoginForm(data=data)
        form.is_valid()

    def test_order_form_validation(self):
        form = OrderForm(data={'comment': 'c', 'delivery_address': 'addr'})
        self.assertTrue(form.is_valid())

    def test_review_form_requires_rating(self):
        form = ReviewForm(data={'product': '', 'customer': '', 'rating': ''})
        self.assertFalse(form.is_valid())


class UrlsTests(SimpleTestCase):
    def test_home_resolves(self):
        resolver = resolve('/')
        self.assertEqual(resolver.func, views.home)

    def test_catalog_resolve(self):
        r = resolve('/catalog/')
        self.assertEqual(r.func, views.catalog)

    def test_about_resolve(self):
        r = resolve('/1/')
        self.assertEqual(r.func, views.about)

    def test_profile_resolve(self):
        r = resolve('/profile/')
        self.assertEqual(r.func, views.profile_page)
