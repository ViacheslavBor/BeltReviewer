from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import *
from django.contrib import messages 
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



def index(request):
	return render(request, 'belt/reglog.html')

def registration(request):
	errors = []
	if len(request.POST['name']) < 2:
		errors.append("Name must be at least 2 characters")
	if len(request.POST['alias']) < 2:
		errors.append("Alias must be at least 2 characters")
	if len(request.POST['password']) < 2:
		errors.append("Password must be at least 2 characters")
	if request.POST['password'] != request.POST['confirm']:
		errors.append("Password and password confirmation don't match. Try again!")
	if not EMAIL_REGEX.match(request.POST['email']):
		messages.error(request,"Invalid Email")
            
	if errors:
		for err in errors:
			messages.error(request, err)
			print(errors)
		return redirect('/')
	
	else:	
		try:
			User.objects.get(email=request.POST['email'])
			messages.error(request, "User with that email already exists.")
			return redirect('/')
		except User.DoesNotExist:
			hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(name=request.POST['name'],\
									alias=request.POST['alias'],\
									password = hashpw,\
									email = request.POST['email'])
			request.session['message'] = "You are registered"
			request.session['user_id'] = user.id
			return redirect('/books')

def login(request):
	try:
		user = User.objects.get(email = request.POST['email'])

		if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
			request.session['user_id'] = user.id
			request.session['message'] = "You are logged in"
			return redirect('/books')
		else:
			messages.error(request, 'Email or password are incorrect')
			return redirect('/')
	except User.DoesNotExist:
		messages.error(request, "Email doesn't exist.")
		return redirect('/')

def books(request):
	context = {
		'user': User.objects.get(id = request.session['user_id']),
		'reviews': Review.objects.order_by("-created_at")[:3],
		'books': Book.objects.filter(reviews__isnull=False),
		'all_books':Book.objects.all()
	}    
	return render(request, 'belt/home.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')

def add_book(request):
	context = {
		'all_authors': Author.objects.all()
	}
	return render(request, 'belt/add.html', context)

def upload(request):
	if request.POST.get('new_author') == "":
		author = Author.objects.get(id=request.POST.get('author'))
	else:
		author = Author.objects.create(name=request.POST.get('new_author', False))
	user = User.objects.get(id=request.session['user_id'])
	book = Book.objects.create(title=request.POST.get('title', False), authors=author, created_by=user)
	Review.objects.create(text=request.POST['text'], rating=request.POST['rating'], books=book, created_by=user)
	return redirect("/books/{}".format(book.id))
	
def book_info(request, id):
	book = Book.objects.get(id=id)
	reviews = book.reviews.all()
	
	context = {
		'current_book': book,
		'all_reviews': reviews
		
	}
	return render(request, 'belt/bookpage.html', context)

def side_review(request, id):
	book = Book.objects.get(id=id)
	created_by = User.objects.get(id=request.session['user_id'])
	Review.objects.create(text=request.POST['comment'], rating=request.POST['rating'], books=book, created_by=created_by)
	return redirect("/books/{}".format(book.id))

def delete_review(request, id):
	review = Review.objects.get(id=id)
	book_id = review.books.id
	review.delete()
	
	
	return redirect('/books/{}'.format(book_id))

