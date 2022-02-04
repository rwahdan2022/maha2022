from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	bio = models.TextField()
	profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
	wesite_url = models.CharField(max_length=255, null=True,blank=True)	
	facebook_url = models.CharField(max_length=255, null=True,blank=True)
	twitter_url = models.CharField(max_length=255, null=True,blank=True)
	instagram_url = models.CharField(max_length=255, null=True,blank=True)
	pinterest_url = models.CharField(max_length=255, null=True,blank=True)

	def __str__(self):
		return str(self.user)


class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name	


class Product(models.Model):
	name = models.CharField(max_length=500, null=True)
	price = models.FloatField()
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=True, null=False)
	digital = models.BooleanField(default=True, null=True, blank=False)
	image = models.ImageField(null=True, blank=True)
	video_name= models.CharField(max_length=500)
	video_file= models.FileField(upload_to='videos/', null=True, verbose_name="")
	video_demo= models.FileField(upload_to='videos_demo/', null=True, verbose_name="")
	
	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	payment_date = models.DateTimeField(blank=True, null=True)
	complete = models.BooleanField(default=False,null=True,blank=False)
	transaction_id = models.CharField(max_length=200, null=True)
	image = models.ImageField(null=True, blank=True)
	pay_confirm = models.BooleanField(default=False,null=True,blank=False)

	def __str__(self):
		return str(self.id)

	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		total = round(total, 0)
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		total = round(total, 0)
		return total

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	quantity = models.IntegerField(default=0, null=True,blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		total = round(total, 0)
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	address = models.CharField(max_length=200, null=True)
	city = models.CharField(max_length=200, null=True)
	state = models.CharField(max_length=200, null=True)
	zipcode = models.CharField(max_length=200, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address