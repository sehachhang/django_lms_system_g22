from datetime import date
import uuid
from django.db import models
from django.urls import reverse
from django.conf import settings

# Model: Genre
class Genre(models.Model):
    name = models.CharField(max_length=20, help_text="Enter Book's Genre name")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genre-detail", kwargs={"pk": self.pk})

class Language(models.Model):
    L_name = models.CharField(max_length=20, help_text="Enter Book's Language")

    class Meta:
        ordering = ['L_name']

    def __str__(self):
        return self.L_name

    def get_absolute_url(self):
        return reverse("language-detail", kwargs={"pk": self.pk})


class Book(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField(
        'ISBN', max_length=13, unique=True,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, blank=True)  # Use string reference

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"pk": self.pk})
    
    def displayGenre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        genres = self.genre.all() # Retrieve all genres associated with the book instance
        genre_names = [genre.name for genre in genres] # Create a list of genre names
        return ', '.join(genre_names) # Join the list into a single string separated by commas
    
    displayGenre.short_description = 'Genre' # Set the column name in the admin interface

class Author(models.Model):
    A_name = models.CharField(max_length=20, help_text="Enter Author's Name")
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    class Meta:
        ordering = ['A_name']

    def __str__(self):
        return self.A_name

    def get_absolute_url(self):
        return reverse("author-detail", kwargs={"pk": self.pk})


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across the whole library")
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=False,
        default='m',
        help_text='Book availability'
    )

    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)

    class Meta:
        ordering = ['due_back']

    def get_absolute_url(self):
        return reverse("bookinstance-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.id} ({self.book})'