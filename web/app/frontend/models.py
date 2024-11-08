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
