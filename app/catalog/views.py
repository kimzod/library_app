from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic


def index(request):

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'catalog/index.html', context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'catalog/author_list.html'


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'
