from django.db import models

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    photoUrl = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    text = models.TextField(max_length=4096)
        
def __str__(self):
    return self.name


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    chatId = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    address = models.TextField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class OrderStatus(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    localDateTime = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.client.name

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    productName = models.CharField(max_length=255)
    productPrice = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.productName
