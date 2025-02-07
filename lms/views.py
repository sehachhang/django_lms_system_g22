from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Language
# Create your views here.
def home(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    '''num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_languages = Language.objects.all().count()
    '''
    playload = {
        'numbooks': num_books,
        'numinstances': num_instances,
    }
    return render(request,'home.html',context=playload)

def aboutUs(request):
    return render(request,'about-us.html')

