from rest_framework import serializers
from .models import Book, Author, User, Category

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'gender', 'user_type',)
        
class AuthorSerializer(serializers.ModelSerializer):
    author_details = UserDetailSerializer()
    class Meta:
        model = Author
        fields = ('author_details', 'author_identification_name',)
    
    def create(self, validated_data):
        author_details = validated_data.get('author_details')
        user_type = int(author_details["user_type"])
        author_identification_name = validated_data.pop('author_identification_name')
        user_obj = User.objects.create(
            first_name=author_details["first_name"],
            last_name=author_details["last_name"],
            email=author_details["email"],
            username=author_details["username"],
            gender=int(author_details["gender"]),
            user_type=int(author_details["user_type"])
        )
        password = "User@123"
        if password is not None:
            user_obj.set_password(password)
        # checking if the new user is of type author
        if user_type==1:
            author = Author.objects.create(
                        author_details=user_obj,
                        author_identification_name=author_identification_name
                        )
        return author
    
    def update(self, instance, validated_data):
        author_details = validated_data.get('author_details')
        first_name=author_details["first_name"]
        last_name=author_details["last_name"]
        gender=int(author_details["gender"])
        user_type=int(author_details["user_type"])
        user_id = int(validated_data.get('user_id'))
        author_identification_name = validated_data.pop('author_identification_name')
        user_obj = User.objects.filter(
            id=user_id
        ).update(
            first_name=author_details["first_name"],
            last_name=author_details["last_name"],
            gender=int(author_details["gender"]),
            user_type=int(author_details["user_type"])
        )
        if user_type==1:
            author = Author.objects.filter(
                        author_details=User.objects.get(id=user_id)
                        ).update(
                            author_identification_name=author_identification_name
                        )
        return author   

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('genre', 'genre_description')

class BookSerializer(serializers.ModelSerializer):
    genre = CategorySerializer(required=False)
    author = AuthorSerializer(many=True)
    class Meta:
        model = Book
        fields = ('title', 'description', 'number_of_pages', 'release_date', 'genre', 'author',)

class BookFilterSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    number_of_pages = serializers.IntegerField(required=False)
    release_date = serializers.DateTimeField(format=None,input_formats=['%Y-%m-%d',], required=False)
    author = serializers.IntegerField(required=False)

class GetFiltersSerializer(serializers.Serializer):
    filters = BookFilterSerializer(required=False)

    @classmethod
    def validate(cls, attrs):
        return attrs

class AuthorFilterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)

class GetAuthorFiltersSerializer(serializers.Serializer):
    filters = AuthorFilterSerializer(required=False)

    @classmethod
    def validate(cls, attrs):
        return attrs

class AddBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'description', 'number_of_pages', 'release_date', 'genre', 'author',)
    
    def create(self, validated_data):
        author = validated_data.pop('author')
        book_obj = Book.objects.create(**validated_data)
        if author:
            for each in author:
                book_obj.author.add(each)
        return book_obj

    def update(self, instance, validated_data):
        author = validated_data.pop('author')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.number_of_pages = validated_data.get('number_of_pages', instance.number_of_pages)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.save()
        if author:
            instance.author.clear()
            for each in author:
                instance.author.add(each)
        return instance


