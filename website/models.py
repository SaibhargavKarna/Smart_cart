from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    product_category=models.CharField(max_length=50)
    product_brand=models.CharField(max_length=50)
    product_name=models.CharField(max_length=150)
    product_image=models.URLField(max_length=300)
    product_price=models.DecimalField(max_digits=7,decimal_places=0)
    product_description=models.CharField(max_length=500,null=True,blank=True)
    product_rating=models.DecimalField(max_digits=2,decimal_places=1,null=True,blank=True)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping=True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total
    

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=0)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.product_price * self.quantity
        return total
    

class ShippingAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=50)
    pincode=models.CharField(max_length=10)
    country=models.CharField(max_length=50)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class paymentDetails(models.Model):
    name=models.CharField(max_length=100)
    amount=models.CharField(max_length=20)
    order_id=models.CharField(max_length=100,blank=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False)

    