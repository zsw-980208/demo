from django.urls import path

from api import views

urlpatterns = [
    path("books/", views.BookAPIVIew.as_view()),
    path("books/<str:id>/", views.BookAPIVIew.as_view()),

    path("book_pub/", views.BookAPIVIew2.as_view()),
    path("book_pub/<str:id>/", views.BookAPIVIew2.as_view()),

    path("v2/books/", views.BookAPIVIewV2.as_view()),
    path("v2/books/<str:id>/", views.BookAPIVIewV2.as_view()),
]
