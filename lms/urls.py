from django.urls import path
from . import views
from .views import AuthorDeleteView

urlpatterns = [
path('', views.home, name='home'),
]
urlpatterns+= [
path('books/', views.BookListView.as_view(), name='books'),
path("book/<int:pk>", views.BookDetailView.as_view(), name='book-detail')
]

urlpatterns+= [
    path("bookintance_list/", views.BookInstanceListView.as_view(), name='bookintance_list'),
    path("bookintance_detail/<uuid:pk>",views.BookInstanceDetailView.as_view(), name="bookinstance-detail"),
    path("bookinstance/",views.BookIntanceCreateView.as_view(), name="bookinstance-create"),
    path("mybooks/", views.BorrowedBooksByUserListView.as_view(),name="mybooks"),
    path("all-borrowed", views.BorrowedAllBooksListView.as_view(),name="all-borrowed"),
]
#For bookintance Model -- renew Due_back date
urlpatterns+=[
    path('book/<uuid:pk>/renew-date/',views.renew_user_book_due_back_date, name="renew-user-book-due-back-date")

]

urlpatterns+=[
    path("genres/", views.GenrelistView.as_view(), name="genres"),
]

urlpatterns+=[
    path("languages/", views.LanguagelistView.as_view(), name='languages')
]

urlpatterns+=[
    path('authors/',views.AuthorListView.as_view(),name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/create', views.AuthorCreateView.as_view(), name="author-create"),
    path('author/<int:pk>/update', views.AuthorUpdateView.as_view(), name="author-update"),
    path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
]

#Search Box
urlpatterns += [
    path('search/', views.search_book, name='book-search'),
]



