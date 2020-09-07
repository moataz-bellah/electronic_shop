from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.urls import reverse
from decimal import Decimal
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Client(models.Model):
    user  = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length = 11)
    email = models.EmailField(blank = True)
    def __str__(self):
        return f"{self.user} {self.phone} "
def create_client(sender,**kwargs):
    if kwargs['created']:
        user_client=Client.objects.create(user=kwargs['instance'])
post_save.connect(create_client,sender=User)
class Category(models.Model):
    super_category = models.ForeignKey('self',limit_choices_to = {'super_category__isnull':True},on_delete = models.CASCADE,blank = True, null = True)
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='name')
    image = models.ImageField(upload_to="categories", blank=True)
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"
class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='name')
    image = models.ImageField(upload_to="products", blank=True)
    brand = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
class ProductAlternative(models.Model):
    product      = models.ForeignKey(Product,on_delete = models.CASCADE,related_name = 'main_product')
    alternatives = models.ManyToManyField(Product)
    
    def __str__(self):
        return self.product.name


class Order(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    date         = models.DateTimeField(auto_now_add = True)
    total_price  = models.PositiveIntegerField(default = 0)
    paid         = models.BooleanField(default = False)
    ordered      = models.BooleanField(default = False)
    def __str__(self):
        return f"{self.user} "
    def get_total_cost(self):
        data=OrderItem()
        self.total=0
        for x in data:
            self.total+=x.total_cost()
        return sum(data.get_cost() for item in self.items.all())
class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    orders=models.ForeignKey(Order,on_delete=models.CASCADE,related_name = 'items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name = 'item')
    quantity = models.IntegerField(default = 1)
    comment = models.TextField(blank = True)
    total_price=models.PositiveIntegerField(default = 0)
    def __str__(self):
        return f"{self.product} {self.quantity} "
    def get_cost(self):
        return self.product.price*self.quantity
class total_cost_after_delevry(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_cost=models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.user.username} {self.total_cost}"
class messages(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.TextField(blank=True)
    def __str__(self):
        return f"{self.user} {self.message}"
