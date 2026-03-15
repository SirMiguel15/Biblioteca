from django.db import models
from django.contrib.auth.models import User
from catalog.models import Book
# Create your models here.

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, verbose_name="Libro")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuario")
    start_date = models.DateField(auto_now_add=True, verbose_name="Fecha de préstamo")
    due_date = models.DateField(verbose_name="Fecha de devolución")
    end_date = models.DateField(null=True, blank=True, verbose_name="Fecha de devolución real")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return f"{self.user} - {self.book} - {'Activo' if self.is_active else 'Devuelto'}"
    
class Fine(models.Model):
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE)
    late_days = models.IntegerField()
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Multa de {self.late_days} días - ${self.fine_amount}"
    