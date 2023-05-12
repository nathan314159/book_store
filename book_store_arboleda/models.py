from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
 
# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=200,null=True)
    Author=models.CharField(max_length=200,null=True)
    Price=models.IntegerField()
    Edition=models.IntegerField()
 
    def __str__(self):
        return str(self.title)
 
class Cart(models.Model): 
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE) 
    books=models.ManyToManyField(Book)
    book_count = models.PositiveIntegerField(default=0)
    def __str__(self):
        return str(self.user)

def update_book_count(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        instance.book_count = instance.books.count()
        instance.save()
m2m_changed.connect(update_book_count, sender=Cart.books.through)

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    total = models.DecimalField(max_digits=8, decimal_places=2)
   
class Payment(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()
    payment_method = models.CharField(max_length=50)
    

class Author(models.Model):
    name = models.CharField(max_length=20,null=True)
    last_name = models.CharField(max_length=20,null=True)
    born = models.DateField()
    death = models.DateField(null=True, blank=True)
    books = models.ManyToManyField('Book')


class Wishlist:
    pass

class Discount:
    pass

class Rating:
    pass

class Review:
    pass

class Category:
    pass