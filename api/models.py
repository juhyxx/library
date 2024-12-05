from django.db import models


class LibUser(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Loan(models.Model):
    user = models.ForeignKey(LibUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} borrowed {self.book.title}"
