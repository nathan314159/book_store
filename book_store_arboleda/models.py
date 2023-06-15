from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from decimal import Decimal
 
# Create your models here.
def default_price():
    return Decimal('0.00')

class Book(models.Model):
    title=models.CharField(max_length=200,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=default_price)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE, null = True)
    authors = models.ManyToManyField('Author')  
    
    def __str__(self):
        author_names = ", ".join(author.name for author in self.authors.all())
        return f'{self.title} (Authors: {author_names})'

   

 
class Cart(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    books=models.ManyToManyField(Book)
    book_count = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def empty_cart(self):
        self.books.clear()
        self.book_count = 0
        self.save()
    
    def update_total_amount(self):
        total = 0
        for book in self.books.all():
            total += book.price
        self.total_amount = total
        self.save()
        
    def save(self, *args, **kwargs):
        self.book_count = self.books.count()  # Update the book count
        super().save(*args, **kwargs)
    
    def __str__(self):
        book_names = ', '.join([str(book) for book in self.books.all()])
        return f"Books: {book_names}"


def update_book_count(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        instance.book_count = instance.books.count()
        instance.save()
m2m_changed.connect(update_book_count, sender=Cart.books.through)

   
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    payment_method = models.CharField(max_length=50)


class Invoice(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    status_revision = models.BooleanField(default=False)
    


class Invoice_detail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE) 
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Invoice detail {self.invoice.id}"


class Author(models.Model):
    name = models.CharField(max_length=20,null=True)

    

class Stock(models.Model):
    total_copies = models.IntegerField(default=0)
    copies_in_stock = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.total_copies}'

    def decrease_stock(self, num_copies):
        if self.copies_in_stock >= num_copies:
            self.copies_in_stock -= num_copies
            self.save()
        else:
            raise ValueError("Not enough copies in stock.")   
        
    def increase_stock(self, num_copies):
        self.copies_in_stock += num_copies
        self.total_copies += num_copies
        self.save()
        
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"