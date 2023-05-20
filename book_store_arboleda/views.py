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
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    context={'books':books, 'cart':cart}
 
    return render(request,'book_store_arboleda/home.html',context)
    

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
    form=Createbookform()
    if request.method=='POST':
        form=Createbookform(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
 
    context={'form':form}
    return render(request,'book_store_arboleda/addbook.html',context)





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
        print(context)
        return render(request, 'book_store_arboleda/viewcart.html', context)

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
    form = Createbookform(request.POST or None, instance=book)
    if form.is_valid():
        book = form.save() # save the form instance to the book object
        book.save() # save the book object to the database
        return redirect('/', id=pk)
    return render(request, 'book_store_arboleda/updateBook.html', {'form': form})



@login_required
def payment(request, cart_id):
    print(request.build_absolute_uri())
    print('cart_id ---->', cart_id)  

    context = {'cart_id':cart_id}
    return render(request, 'book_store_arboleda/payment.html', context)


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

