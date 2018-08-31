from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Author(models.Model):
	name = models.CharField(max_length=255, default=None)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
	title = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(User, related_name='books')
	authors = models.ForeignKey(Author, related_name = "books")

class Review(models.Model):
	text = models.CharField(max_length=255)
	rating = models.IntegerField(
		default=0,
		validators=[MaxValueValidator(5), MinValueValidator(1)]
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	books = models.ForeignKey(Book, related_name='reviews')
	created_by = models.ForeignKey(User, related_name='reviews')


	