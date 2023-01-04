from django.db import models
from django.contrib.auth.models import AbstractUser
from .choice import UserTypes, Gender

# Create your models here.

# Extending the existing default user model
class User(AbstractUser):
	user_type = models.PositiveSmallIntegerField(default=UserTypes.OTHER, choices=UserTypes.CHOICES)
	gender = models.PositiveSmallIntegerField(default=Gender.UNKNOWN, choices=Gender.CHOICES)

	class Meta(AbstractUser.Meta):
		abstract = False

	def __str__(self):
		return self.username


# Author model to store author details
class Author(models.Model):
	author_details = models.ForeignKey(
        User, on_delete=models.CASCADE)
	author_identification_name = models.CharField(max_length=30, unique=True) 

	def __str__(self):
		return self.author_identification_name


# Category model to record the genre details
class Category(models.Model):
	genre = models.CharField(max_length=30, unique=True)
	genre_description = models.TextField()

	def __str__(self):
		return self.genre


# Book model for storing the details for the books
class Book(models.Model):
	title = models.CharField(max_length=256, unique=True)
	description = models.TextField()
	number_of_pages = models.IntegerField(default=1)
	release_date = models.DateTimeField(auto_now=True, null=True)
	author = models.ManyToManyField(Author)
	genre = models.ForeignKey(Category, on_delete=models.CASCADE)

	class Meta:
		unique_together = (
            'title', 'genre')
	def __str__(self):
		return self.title





