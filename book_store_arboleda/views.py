from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

def home(request):
    books=Book.objects.all()
    context={'books':books}
 
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
    carts = Cart.objects.filter(user=request.user)
    context = {'carts': carts}
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
    cart.book_count -= 1
    cart.save()
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


