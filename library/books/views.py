from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Author, Category, Book
from django.shortcuts import get_object_or_404
from .serializers import BookSerializer, AuthorSerializer, \
    GetFiltersSerializer, GetAuthorFiltersSerializer, AddBookSerializer

class BooksView(APIView):
    """
    API for add/edit/get/delete books
    """
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({
            "books":serializer.data
        })
    
    def post(self, request):
        # Create a book from the request data
        serializer = AddBookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            book_saved = serializer.save()
        return Response({"success": "Book '{}' created successfully".format(book_saved.title)})

    def put(self, request, pk):
        saved_book = get_object_or_404(Book.objects.all(), pk=pk)
        serializer = AddBookSerializer(instance=saved_book, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            book_saved = serializer.save()
        return Response({"success": "Book '{}' updated successfully".format(book_saved.title)})
    
    def delete(self, request, pk):
        # Get object with this pk
        book = get_object_or_404(Book.objects.all(), pk=pk)
        authors = book.author.all()
        if authors:
            book.author.clear()
            for each in authors:
               if not Book.objects.filter(
                   author__author_identification_name=each.author_identification_name
                   ).exists():
                   User.objects.filter(
                       id=each.author_details.id
                   ).delete()
        book.delete()
        return Response({"message": "Book with id `{}` has been deleted.".format(pk)},status=204)

class AuthorsView(APIView):
    """
    API for add/edit/get/delete authors
    """
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response({
            "authors":serializer.data
        })
    
    def post(self, request):
        # Create an Author from the request data
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            author_saved = serializer.save()
        return Response({"success": "Author '{}' created successfully".format(author_saved.author_identification_name)})

    def put(self, request, pk):
        # saved_user = get_object_or_404(User.objects.all(), pk=pk)
        saved_user = get_object_or_404(User.objects.all(), pk=pk)
        author_details = request.data.get('author_details')
        first_name=author_details["first_name"]
        last_name=author_details["last_name"]
        gender=int(author_details["gender"])
        user_type=int(author_details["user_type"])
        author_identification_name = request.data.get('author_identification_name')
        user_obj = User.objects.filter(
            id=pk
        ).update(
            first_name=author_details["first_name"],
            last_name=author_details["last_name"],
            gender=int(author_details["gender"]),
            user_type=int(author_details["user_type"])
        )
        if user_type==1:
            author = Author.objects.filter(
                        author_details=User.objects.get(id=pk)
                        ).update(
                            author_identification_name=author_identification_name
                        )
        return Response({"success": "User updated successfully"})
    
    def delete(self, request, pk):
        # Get object with this pk
        author = get_object_or_404(Author.objects.all(), pk=pk)
        author = Author.objects.get(id=pk)
        if not Book.objects.filter(
            author__author_identification_name=author.author_identification_name
            ).exists():
            User.objects.filter(
                id=author.author_details.id
            ).delete()
            return Response({"message": "Author with id `{}` has been deleted.".format(pk)},status=204)
        return Response({"message": "Author with id `{}` deletetion denied because the author associated in a book.".format(pk)},status=204)

class GetBookFiltersView(APIView):
    """
    API for search a books based titile, number_of_pages, release_date, author individually or all together
    """
    def post(self, request, *args, **kwargs):
        """
        Get All the books for filters
        """
        serializer = GetFiltersSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            filters = dict(serializer.data.get('filters', {}))
            if not filters:
                books = Book.objects.all()
            else:
                books = Book.objects.all()
                for each_filter, filter_params in filters.items():
                    if(str(each_filter))=="title":
                        books = books.filter(title__icontains=str(filter_params))
                    elif(str(each_filter))=="number_of_pages":
                        books = books.filter(number_of_pages__icontains=int(filter_params))
                    elif(str(each_filter))=="release_date":
                        year = str(filter_params).split("-")[0]
                        books = books.filter(release_date__year=year)
                    elif(str(each_filter))=="author":
                        books = books.filter(author=int(filter_params))
                    else:
                        pass
            serializer = BookSerializer(books, many=True)
            return Response({
                "books":serializer.data
            })
            # return Response(filters, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAuthorFiltersView(APIView):
    def post(self, request, *args, **kwargs):
        """
        API for search an author based first_name, last_name, email individually or all together
        """
        serializer = GetAuthorFiltersSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            filters = dict(serializer.data.get('filters', {}))
            if not filters:
                authors = Author.objects.all()
            else:
                authors = Author.objects.all()
                for each_filter, filter_params in filters.items():
                    if(str(each_filter))=="first_name":
                        authors = authors.filter(author_details__first_name__icontains=str(filter_params))
                    elif(str(each_filter))=="last_name":
                        authors = authors.filter(author_details__last_name__icontains=str(filter_params))
                    elif(str(each_filter))=="email":
                        authors = authors.filter(author_details__email__icontains=str(filter_params))
                    else:
                        pass
            serializer = AuthorSerializer(authors, many=True)
            return Response({
                "authors":serializer.data
            })
            # return Response(filters, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      






