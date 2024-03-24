from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null= True, blank=False)
    image  = models.ImageField(null=True, blank=True)

    def  __str__(self):
        return self.name
    
    @property
    def imageURL(self):
       try:
           url = self.image.url
       except:
           url = ''
       return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
                # Returns the string representation of the model.
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.get_total  for item in orderitem])
        return total
    
    @property
    def get_cart_items(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity  for item in orderitem])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, blank=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total =  self.quantity * self.product.price
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, blank=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, blank=True)
    address = models.CharField(max_length=200, null= False)
    city = models.CharField(max_length=100, null= False)
    state = models.CharField(max_length=50, null= True)
    zip = models.CharField(max_length=20, null= False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class AddCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)       #Each cart instance is associated with a single user. 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)     #Each cart instance is associated with a single pet product. Similarly, the on_delete=models.CASCADE argument means that if the referenced 
    quantity = models.PositiveIntegerField(default=1)              # Quantity cannot be negative so we have used PositiveIntegerField

    def __str__(self):
        return str(self.id)