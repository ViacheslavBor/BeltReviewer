from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^registration$', views.registration),
	url(r'^login$', views.login),
	url(r'^books$', views.books),
	url(r'^logout$', views.logout),
	url(r'^books/add$', views.add_book),
	url(r'^upload$', views.upload),
	url(r'^books/(?P<id>\d+)$', views.book_info),
	url(r'^side_review/(?P<id>\d+)$', views.side_review),
	url(r'^delete_review/(?P<id>\d+)$', views.delete_review),
]