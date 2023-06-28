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
    book = get_object_or_404(Book, id=pk)
    user_id = request.user.id
    cart = Cart.objects.filter(user_id=user_id).first()  # Get the cart for the user
    
    if not cart:
        cart = Cart(user_id=user_id)

        cart.save()  # Save the newly created cart
    
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
    customer_form = CreateCustomerForm()
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        customer_form = CreateCustomerForm(request.POST)
        if payment_form.is_valid() and customer_form.is_valid():
            payment = payment_form.save(commit=False)
            try:
                existing_customer = Customer.objects.get(user=request.user)
                # Update the existing customer fields
                existing_customer.first_name = customer_form.cleaned_data['first_name']
                existing_customer.last_name = customer_form.cleaned_data['last_name']
                existing_customer.phone_number = customer_form.cleaned_data['phone_number']
                existing_customer.email = customer_form.cleaned_data['email']
                existing_customer.save()
                customer = existing_customer
            except Customer.DoesNotExist:
                # Create a new customer
                customer = customer_form.save(commit=False)
                customer.user = request.user
                customer.save()

            payment.customer = customer
            payment.save()
            
            # Hacer la operacion para el stock ej 50-1  para cada libro
            #
            # Pass customer information to the inventory function
            inventory(request, customer.id)
                                                                        
            
            return redirect('invoice', payment_id=payment.id, customer_id=customer.id)
    else:
        payment_form = PaymentForm()
        try:
            existing_customer = Customer.objects.get(user=request.user)
            # Customer exists, pre-fill the form with the existing data
            initial_data = {
                'first_name': existing_customer.first_name,
                'last_name': existing_customer.last_name,
                'phone_number': existing_customer.phone_number,
                'email': existing_customer.email,
            }
            customer_form = CreateCustomerForm(initial=initial_data)
        except Customer.DoesNotExist:
            # Customer does not exist, continue with an empty form
            pass

    context = {
        'payment_form': payment_form,
        'customer_form': customer_form
    }
    return render(request, 'book_store_arboleda/payment.html', context)

def invoice_detail(request, invoice_id, book_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice_details = Invoice_detail.objects.filter(invoice=invoice)
    books = [invoice_detail.book for invoice_detail in invoice_details]
    book = Book.objects.get(id=book_id)
    
    user = request.user
    cart = Cart.objects.get(user=user)
    
    

    context = {
        'invoice': invoice,
        'books': books,
        'book': book,
        'cart': cart,
    }
    print('--- book id: ', book_id)
    print('--- invoice id: ', invoice)
    return render(request, 'book_store_arboleda/invoice_detail.html', context)


def invoice(request, payment_id, customer_id):
    payment = Payment.objects.get(id=payment_id)
    customer = Customer.objects.get(id=customer_id)
    user = request.user

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = None

    books = cart.books.all() if cart else []


    total_amount = cart.total_amount if cart else 0  # Get the total_amount from Cart

    # Save the invoice in the database
    new_invoice = Invoice.objects.create(
        payment=payment,
        customer=customer,
    )

    # Create and save the invoice details <------- Inventory
    invoice_details = []
    for book in books:
        invoice_detail = Invoice_detail.objects.create(invoice=new_invoice, book=book, amount=1)
        Stock.objects.get(id = book.id).decrease_stock(1)
        invoice_details.append(invoice_detail)
        
        
    # Clear the cart after creating the invoice
    cart.empty_cart()

    context = {
        'payment': payment,
        'user': user,
        'payment_id': payment_id,
        'books': books,
        'total_amount': total_amount,
        'customer': customer,
  


    }
    

    return render(request, 'book_store_arboleda/invoice.html', context)


def inventory(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    inventory = Inventory.objects.create(customer=customer)
    
    stock_books = Book.objects.filter(stock__isnull=False)  # Retrieve books that have a stock relationship
    
    inventory_detail_list = []
    for book in stock_books:
        stock = book.stock
        inventory_details = Inventory_detail.objects.filter(book=book)

        for inventory_detail in inventory_details:
            inventory_detail.amount = stock.copies_in_stock
            inventory_detail.save()
            inventory_detail_list.append(inventory_detail)

    
    context = {
        'customer': customer,
        'inventory': inventory,
        'inventory_detail_list': inventory_detail_list,
    }
    
    return render(request, 'book_store_arboleda/inventory.html', context)



def create_customer(request):
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                customer = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                customer = None

            if customer:
                # If customer with the email already exists, update the existing customer
                customer.first_name = form.cleaned_data.get('first_name')
                customer.last_name = form.cleaned_data.get('last_name')
                customer.phone_number = form.cleaned_data.get('phone_number')
                customer.save()
            else:
                # If customer with the email doesn't exist, create a new customer
                form.save()

            # Redirect or return response
    else:
        form = CreateCustomerForm()

    # Render the form in the template


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
    


def inventory_detail(request, inventory_id, book_id):
    print("--- inventory_detail function called")
    
    inventory = get_object_or_404(Inventory, id=inventory_id)
    print("--- inventory_id:", inventory_id)
    print("--- inventory:", inventory)
    
    inventoryDetails = Inventory_detail.objects.filter(inventory=inventory)
    print("--- inventoryDetails:", inventoryDetails)
    
    books = [inventory_details.book for inventory_details in inventoryDetails]
    print("--- books:", books)
    
    book = Book.objects.get(id=book_id)
    print("--- book_id:", book_id)
    print("--- book:", book)
    
    user = request.user
    print("--- user:", user)
    
    cart = Cart.objects.get(user=user)
    print("--- cart:", cart)
    
    context = {
        'inventory': inventory,
        'books': books,
        'book': book,
        'cart': cart,
    }
    
    print("--- context:", context)
    
    return render(request, 'book_store_arboleda/invoice_detail.html', context)
