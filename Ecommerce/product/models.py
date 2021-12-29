from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
	name = models.CharField(max_length=50, null=False, blank=False)
	slug = models.SlugField(unique=True, default='slug')

	@staticmethod
	def get_all_categories():
		return Category.objects.all()

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('product_by_category', args=[self.slug])

class Brand(models.Model):
	name = models.CharField(max_length=50, null=False, blank=False)
	description = models.CharField(max_length=200)
	image = models.ImageField(upload_to='photos', max_length=254)

	def __str__(self):
		return self.name

class Gender(models.Model):
	name = models.CharField(max_length=50, null=False, blank=False) 

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=50, null=False, blank=False)
	product_code = models.CharField(max_length=50)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
	brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
	gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
	description = models.CharField(max_length=1000)
	price = models.PositiveIntegerField(default=0)
	currency = models.CharField(max_length=20)
	discount = models.IntegerField(default=0)
	color = models.CharField(max_length=20, null=True, blank=True)
	size = models.CharField(max_length=20, null=True, blank=True)
	condition = models.CharField(max_length=20, null=True, blank=True)
	model = models.CharField(max_length=30, null=True, blank=True)
	is_available = models.CharField(max_length=20, null=True, blank=True)
	rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.featured.url
		except:
			url = ''
		print('URL:', url)
		return url
	
	@property
	def discount_price(self):
		if self.discount > 0:
			discounted_price = self.price - self.price * self.discount / 100
			return discounted_price    

	@staticmethod
	def get_products_by_id(ids):
		return Product.objects.filter(id__in=ids)

	@staticmethod
	def get_all_products():
		return Product.objects.all()

	@staticmethod
	def get_all_products():
		return Product.objects.all()

	@staticmethod
	def get_products_by_categoryid(category_id):
		if category_id:	
			return Product.objects.filter(category=category_id)
		else:
			return Product.get_all_products()

class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
	image = models.ImageField(null=True, blank=True)
	feature = models.BooleanField(default=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	thumbnail = models.BooleanField(default=False)

	def __str__(self):
		return self.product.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		print('URL:', url)
		return url




class Customer(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField()
	phone = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=10, null=True)
	zip_code = models.CharField(max_length=10, null=True)



	def __str__(self):
		return self.name



class Cart(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	total = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return "Cart:" + str(self.id)


ORDER_STATUS = (
	("Order Received", "Order Received"),
	("Order Processing", "Order Processing"),
	("On the Way", "On the Way"),
	("Order Cancelled", "Order Cancelled"),
	)

class Order(models.Model):
	cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
	ordered_by = models.CharField(max_length=200)
	shipping_address = models.CharField(max_length=200)
	mobile = models.CharField(max_length=20)
	email = models.EmailField(null=True, blank=True)
	city = models.CharField(max_length=20, null=True)
	zip_code = models.CharField(max_length=20, null=True)

	subtotal = models.PositiveIntegerField()
	discount = models.PositiveIntegerField()
	total = models.PositiveIntegerField()
	order_status = models.CharField(max_length=50, choices=ORDER_STATUS)

	def __str__(self):
		return "Order: " + str(self.id)



class CartProduct(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	rate = models.PositiveIntegerField()
	quantity = models.PositiveIntegerField()
	subtotal = models.PositiveIntegerField()

	def __str__(self):
		return "Cart"+ str(self.cart.id) + "ProductCart: "+ str(self.id)



class SliderImage(models.Model):
	image = models.ImageField(null=True, blank=True)
	title = models.CharField(max_length=30)

	def __str__(self):
		return self.title


class Review(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	comment = models.TextField(max_length=250, null=True, blank=True)
	rate = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.id)