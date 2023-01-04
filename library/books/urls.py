from django.urls import path
from .views import *

urlpatterns = [
    path(
	   'get_books/',
	   BooksView.as_view(),
	   name='get_books'),
    path(
	   'get_authors/',
	   AuthorsView.as_view(),
	   name='get_authors'),
    path('books_get_filters/', 
        GetBookFiltersView.as_view(),
	    name='books_get_filters'),
    path('authors_get_filters/', 
        GetAuthorFiltersView.as_view(),
	    name='authors_get_filters'),
    path('get_books/<int:pk>', 
        BooksView.as_view(),
	    name='get_books'),
    path('get_authors/<int:pk>', 
        AuthorsView.as_view(),
	    name='get_authors')
    
]
