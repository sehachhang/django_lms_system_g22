from pyexpat.errors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic import DetailView
from .models import Author, Book, BookInstance, Genre, Language
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from .forms import Search_Book


# Create your views here.
def home(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    playload = {
        'numbooks': num_books,
        'numinstances': num_instances,
    }
    return render(request,'home.html',context=playload)

class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book

from django.contrib.auth.mixins import LoginRequiredMixin
class BorrowedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "lms/myborrowedbooks.html"
    # Create a function to filter only the specific books borrowed by specific User
    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
        )
class BorrowedAllBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "lms/bookinstance_list_borrowed_all.html"
    permission_required ="lms.can_views_all_borrowed_books"
    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o').order_by('due_back')
        )
class BookInstanceListView(generic.ListView):
    model = BookInstance

class BookInstanceDetailView(generic.ListView):
    model = BookInstance

class BookIntanceCreateView(PermissionRequiredMixin, CreateView):
    model = BookInstance
    fields = "__all__"
    permission_required = 'lms.add_bookinstance'

class GenrelistView(generic.ListView):
    model = Genre

class LanguagelistView(generic.ListView):
    model = Language

#Create operation: CreateView
class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(DetailView):
    model = Author

class AuthorCreateView(PermissionRequiredMixin, CreateView):
    model = Author
    # fields = '__all__' #Optionals: you can use '__all__' value to be able do Create Operation for all fields.
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': "Filled the Date of Author Death. Leave blank if he/she alives"}
    permission_required = 'lms.add_author'

class AuthorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Author
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'lms.change_author'

class AuthorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Author
    permission_required = 'lms.delete_author'
    success_url = reverse_lazy('authors')
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )
#Function for handing renew back date
import datetime
from lms.forms import RenewBookInstanceDate
from django.contrib.auth.decorators import login_required, permission_required
@login_required
@permission_required('lms.can_views_all_borrowed_books', raise_exception=True)
def renew_user_book_due_back_date(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

       # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookInstanceDate(request.POST)

        # Check if the form's data is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to the Successful URL:
            return HttpResponseRedirect(reverse('all-borrowed'))
    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookInstanceDate(initial={'renewal_date': proposed_renewal_date})
    
    playLoads = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'lms/book_instance_renew_date.html',context= playLoads)

def search_book(request):
    form = Search_Book(request.GET)
    search_results = []

    if form.is_valid():

        search_query = form.cleaned_data.get('search_query')
        if search_query:
            search_results = Book.objects.filter(title__icontains=search_query) #Search Book Title

    play_loads = {
        'form': form,
        'search_results': search_results
    }

    return render(request, 'lms/book_search_result.html', context=play_loads)





