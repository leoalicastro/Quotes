from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('home', views.home),
    path('add_quote', views.add_quote),
    path('user/<int:user_id>', views.user),
    path('edit/<int:quote_id>', views.edit),
    path('edit_quote/<int:quote_id>', views.edit_quote),
    path('update_quote/<int:quote_id>', views.update_quote),
    path('my_account/<int:user_id>', views.my_account),
    path('edit_account/<int:user_id>', views.edit_account),
    path('like_quote/<int:quote_id>', views.like_quote),
    path('unlike_quote/<int:quote_id>', views.unlike_quote),
    path('logout', views.logout),
    path('delete/<int:quote_id>', views.delete)
]