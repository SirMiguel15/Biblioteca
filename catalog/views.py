
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Book
from .forms import BookForm

class BookListView(ListView):
    model = Book
    template_name = "catalog/book_list.html"
    context_object_name = "books"
    paginate_by = 10

    def get_queryset(self):
        queryset = Book.objects.all()
        q = self.request.GET.get("q", "")
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(author__name__icontains=q)
            )
        return queryset

class BookDetailView(DetailView):
    model = Book
    template_name = "catalog/book_detail.html"
    context_object_name = "book"
    
class BookCreateView(UserPassesTestMixin, CreateView):
    model = Book
    template_name = "catalog/book_form.html"
    form_class = BookForm
    success_url = reverse_lazy("book-list")

    def test_func(self):
        return self.request.user.is_staff
    
class BookUpdateView(UserPassesTestMixin, UpdateView):
    model = Book
    template_name = "catalog/book_form.html"
    form_class = BookForm
    success_url = reverse_lazy("book-list")

    def test_func(self):
        return self.request.user.is_staff

class BookDeleteView(UserPassesTestMixin, DeleteView):
    model = Book
    template_name = "catalog/book_confirm_delete.html"
    success_url = reverse_lazy("book-list")

    def test_func(self):
        return self.request.user.is_staff
    
