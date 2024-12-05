from django.contrib import admin
from django.urls import path
from api.views.library_view import borrowed, free
from api.views.loans_view import LoansView
from api.views.books_view import BooksView
from api.views.users_view import UsersView

"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", UsersView.as_view(), name="users"),
    path("api/users/<int:id>/", UsersView.as_view(), name="users"),
    path("api/books/", BooksView.as_view(), name="book-list"),
    path("api/books/<int:id>/", BooksView.as_view(), name="book-id"),
    path("api/loans/", LoansView.as_view(), name="loans"),
    path("api/books/free", free, name="loans"),
    path("api/books/borrowed", borrowed, name="loans"),
    
]
