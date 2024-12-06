from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.books_view import BooksView
from api.views.loans_view import LoansView
from api.views.users_view import UsersView

router = DefaultRouter()

router.register(r"books", BooksView, basename="books")
router.register(r"users", UsersView, basename="users")
router.register(r"loans", LoansView, basename="loans")


urlpatterns = [path("api/", include(router.urls)), path("admin/", admin.site.urls)]
