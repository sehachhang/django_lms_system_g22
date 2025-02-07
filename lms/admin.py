from django.contrib import admin
# Register your models here.
from .models import Genre, Book, Language, BookInstance, Author

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','isbn','displayGenre','language','summary')
    list_filter = ('title','author','genre','language')
admin.site.register(Book, BookAdmin)

admin.site.register(Genre)
#admin.site.register(Book)
admin.site.register(Language)
admin.site.register(BookInstance)
admin.site.register(Author)
