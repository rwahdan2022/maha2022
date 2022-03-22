from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.aboutme, name="about-me"),
    path('cart.html/', views.cart, name="cart"),
    path('checkout.html/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('transactions/', views.BeforeTransactions, name="list-transactions"), 
    path('show_transactions/<order>', views.transactions, name="detailed-transactions"), 
    path('add_product/', views.add_product, name="add-product"),
    path('add_cat/', views.add_cat, name="add-cat"),
    path('store.html/', views.store, name="store"),

]