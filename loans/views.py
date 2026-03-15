from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from datetime import date
from .models import Loan, Fine

# Prestamo del libro
class LoanCreateView(LoginRequiredMixin, CreateView):
    model = Loan
    template_name = "loans/loan_form.html"
    fields = ["book", "due_date"]
    success_url = reverse_lazy("my-loans")

    def form_valid(self, form):
        book = form.instance.book
        if not book.is_available:
            form.add_error(None, "Este libro no está disponible para préstamo.")
            return self.form_invalid(form)
        form.instance.user = self.request.user
        book.is_available = False
        book.save()
        return super().form_valid(form)
    
# Devolver el libro prestado
class LoanReturnView(UserPassesTestMixin, UpdateView):
    model = Loan
    template_name = "loans/loan_return.html"
    fields = []
    success_url = reverse_lazy("all-loans")

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        loan = form.instance
        loan.end_date = date.today()
        loan.is_active = False
        loan.save()

        late_days = (loan.end_date - loan.due_date).days
        if late_days > 0:
            Fine.objects.create(
                loan=loan,
                late_days=late_days,
                fine_amount=late_days * 1000
            )

        loan.book.is_available = True
        loan.book.save()
        return super().form_valid(form)
    
# Pretamos
class MyLoansView(LoginRequiredMixin, ListView):
    model = Loan
    template_name = "loans/my_loans.html"
    context_object_name = "loans"

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)

# Todos los prestamos que ve el staff    
class AllLoansView(UserPassesTestMixin, ListView):
    model = Loan
    template_name = "loans/all_loans.html"
    context_object_name = "loans"

    def test_func(self):
        return self.request.user.is_staff
    

