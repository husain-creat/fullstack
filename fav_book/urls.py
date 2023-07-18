from django.urls import path     
from . import views

urlpatterns = [ path('', views.index),
               path('register', views.register),
               path('login', views.login), 
               path('book', views.book), 
               path('add_book', views.add_book),
               path('edit_book/<int:id>', views.edit , name='edit_book'), 
               path('details/<int:id>', views.details,name='details'), 
               path('unfav/<int:book_id>/<int:user_id>', views.unfav,name='unfav'),  
               
                 ]