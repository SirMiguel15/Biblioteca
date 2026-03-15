from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "isbn"]

    def clean_isbn(self):
        isbn = self.cleaned_data.get("isbn")
        if len(isbn) != 10 and len(isbn) != 13:
            raise forms.ValidationError("El ISBN debe tener entre 10 o 13 caracteres")
        return isbn
    
