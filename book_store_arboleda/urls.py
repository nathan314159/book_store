from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path("", views.home, name="home"),
    path('book_list/', views.book_list,name='book_list'),
    path('login/', views.loginPage,name='login'),
    path('viewcart/', views.viewcart, name='viewcart'),
    path('addbook/', views.addbook,name='addbook'),
    path('register/', views.registerPage,name='register'),
    path('logout/', views.logoutPage,name='logout'),
    path('addtocart/<str:pk>', views.addtocart,name='addtocart'),
    path('deleteBook/<str:pk>', views.deleteBook,name='deleteBook'),
    path('updateBook/<str:pk>', views.updateBook,name='updateBook'),
    path('removeBookFromCart/<str:book_id>', views.removeBookFromCart,name='removeBookCustomer'),
    path('payment/', views.payment, name='payment'),
    path('empty_cart_page/', views.empty_cart_page, name='empty_cart_page'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
    path('invoice/<int:payment_id>/', views.invoice, name='invoice'),
    path('invoice_detail/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    # path('sell_book/<int:book_id>/', views.sell_book, name='sell_book'),
    # path('decrease_stock/<int:book_id>/', views.decrease_stock, name='decrease_stock'),

]