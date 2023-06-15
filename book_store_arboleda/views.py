from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from .forms import *
from .models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

def home(request):
    books=Book.objects.all()
    cart = None
    stock = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    context={'books':books, 'cart':cart, 'stock':stock}
    
        # Fetching authors and stock
    authors = Author.objects.all()
    stock = Stock.objects.first()
    context['authors'] = authors
    context['stock'] = stock
 
    return render(request,'book_store_arboleda/home.html',context)
    

def increase_book_stock(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.add_to_stock(1)  # Increase stock by 1
    return redirect('home')

def decrease_book_stock(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.decrease_stock(1)  # Decrease stock by 1
    return redirect('home')

def logoutPage(request):
    logout(request)
    return redirect('/')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            print("working")
            login(request,user)
            return redirect('/')
       context={}
       return render(request,'book_store_arboleda/login.html',context)
   
def registerPage(request):
    form = Createuserform()
    
    if request.method == 'POST':
        form = Createuserform(request.POST)
        if form.is_valid():
            print('form data is valid')
            user = form.save()

            user = user 
            user.save()
            
            print(form.cleaned_data)

            
            return redirect('login')
        else:
            print('form data is not valid')
            for field in form:
                if field.errors:
                    print(f"Error in field {field.name}: {field.errors}")
    context = {
        'form': form,
    }
    
    return render(request, 'book_store_arboleda/register.html', context)


def addbook(request):
    book_form = Createbookform()
    stock_form = CreateStockForm()
    author_form = CreateAuthorForm()
    if request.method == 'POST':
        author_form = CreateAuthorForm(request.POST)
        book_form = Createbookform(request.POST)
        stock_form = CreateStockForm(request.POST)
        if book_form.is_valid() and stock_form.is_valid() and author_form.is_valid():
            book = book_form.save()  # Save the book instance
            stock = stock_form.save(commit=False)  # Save the stock instance without committing to the database yet
            num_books = 0  # start at 0
            
            stock.total_copies += num_books  # Increment the total_copies by the number of books
            stock.copies_in_stock += num_books  # Increment the copies_in_stock by the number of books
            stock.save()  # Now save the stock instance to the database
            
            book.stock = stock  # Associate the stock with the book
            book.save()  # Save the book instance with the updated stock information
            authors = author_form.save()
            book.authors.add(authors)
            return redirect('/')
    else:
        print("Form errors:", book_form.errors, stock_form.errors)

    context = {
        'book_form': book_form,
        'stock_form': stock_form,
        'author_form': author_form
    }

    return render(request, 'book_store_arboleda/addbook.html', context)


 


@login_required
def addtocart(request, pk):
    book = Book.objects.get(id=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.books.add(book)
    messages.success(request, 'The book has been added successfully to the cart!')
    return redirect('viewcart')

def deleteBook(request, pk):
    book = Book.objects.get(id=pk)
    book.delete()
    messages.success(request, 'Book removed from cart successfully!')
    return redirect('/')


def removeBookFromCart(request, book_id):
    cart = Cart.objects.filter(user=request.user).first()
    book = Book.objects.get(id=book_id)
    
    cart.books.remove(book)
    cart.book_count = cart.books.count()  # Update the book count
    cart.save()
    if cart.book_count > 0:
        cart.book_count -= 1
        cart.save()
    else:
        cart.empty_cart()
        return redirect('empty_cart_page')
    messages.success(request, 'Book removed from cart successfully!')
    return redirect('viewcart')


def removeBookUser(request, pk):
    removeBookFromCart(request, pk)
    messages.success(request, 'Book removed from cart successfully!')
    return redirect('viewcart')


def updateBook(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    createbook_form = Createbookform(instance=book)
    stock_form = CreateStockForm(instance=book.stock)
    author_form = CreateAuthorForm(instance=book.authors.first())  # Use Author model instance
    
    if request.method == 'POST':
        createbook_form = Createbookform(request.POST or None, instance=book)
        stock_form = CreateStockForm(request.POST, instance=book.stock)
        author_form = CreateAuthorForm(request.POST, instance=book.authors.first())  # Use Author model instance
        
        if createbook_form.is_valid() and stock_form.is_valid() and author_form.is_valid():
            book = createbook_form.save()  
            
            stock = stock_form.save(commit=False)
            stock.book = book
            stock.save()
            
            author = author_form.save()
            book.authors.clear()  # Clear existing authors
            book.authors.add(author)
            
            return redirect('/')
    
    context = {
        'createbook_form': createbook_form,
        'stock_form': stock_form,
        'author_form': author_form,
    }
    return render(request, 'book_store_arboleda/updateBook.html', context)





def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_store_arboleda/home.html', {'books': books})

def empty_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.empty_cart()
    return redirect('empty_cart_page')

def empty_cart_page(request):
    return render(request, 'book_store_arboleda/emptycart.html')


@login_required
def payment(request):
    user = request.user

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return HttpResponse("Cart not found.")

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = user
            payment.save()
            context = {
                'date': payment.date,
                'payment_method': payment.payment_method,
                'cart': cart
            }
            return redirect('invoice', payment_id=payment.id)
    else:
        form = PaymentForm()

    print("Cart:", cart)
    print("Books in Cart:")
    for book in cart.books.all():
        print(book)

    context = {
        'form': form,
        'cart': cart
    }
    return render(request, 'book_store_arboleda/payment.html', context)




def invoice(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    user = request.user
    invoices = Invoice.objects.filter(payment=payment)

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = None

    books = cart.books.all() if cart else []

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.payment = payment
            invoice.user = user
            invoice.save()

            for book in books:
                invoice_detail = Invoice_detail.objects.create(invoice=invoice, book=book)
                invoice_detail.save()

            # cart.books.clear()  # Empty the cart by removing all books

            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm()
        
    total_amount = cart.total_amount if cart else 0  # Get the total_amount from Cart

    
    context = {
        'payment': payment,
        'user': user,
        'payment_id': payment_id,
        'invoices': invoices,
        'form': form,
        'books': books,
        'total_amount':total_amount,
    }

    # Print books and book_count
    for book in books:
        print(book.title)

    book_count = len(books)
    print("Book Count:", book_count)

    return render(request, 'book_store_arboleda/invoice.html', context)





def invoice_detail(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    invoice_details = Invoice_detail.objects.filter(invoice=invoice)

    user = request.user
    cart = Cart.objects.get(user=user)
    books = cart.books.all()
    
    context = {
        'invoice': invoice,
        'invoice_details': invoice_details,
        'books': books,
        'cart': cart,  # Add the cart object to the context
    }
    print(context)
    cart.empty_cart()
    return render(request, 'book_store_arboleda/invoice_detail.html', context)




@login_required
def viewcart(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_id = cart.id
    if cart.book_count == 0:
        return redirect('empty_cart_page')
    else:
        cart.update_total_amount()
        context = {'cart': cart, 'cart_id': cart_id}
        print(context,)
        return render(request, 'book_store_arboleda/viewcart.html', context)
    


def sell_book(request, book_id):
    # Retrieve the book instance
    book = get_object_or_404(Book, pk=book_id)

    # Sell one copy of the book
    try:
        book.decrease_stock(1)
    except ValueError as e:
        # Handle the case where there are not enough copies in stock
        return HttpResponse(str(e))

    # Perform other operations related to selling the book (e.g., generating an invoice, updating user information, etc.)

    return HttpResponse("Book sold successfully")
