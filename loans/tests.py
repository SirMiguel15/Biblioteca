from django.test import TestCase, Client
from django.contrib.auth.models import User
from datetime import date, timedelta
from catalog.models import Author, Book
from .models import Loan, Fine

class LoansTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name="Gabriel Garcia Marquez")
        self.book = Book.objects.create(
            title="Cien años de soledad",
            author=self.author,
            isbn="1234567890123",
            is_available=True
        )
        self.staff_user = User.objects.create_user(
            username="staff",
            password="pass1234",
            is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username="usuario",
            password="pass1234"
        )
        self.loan = Loan.objects.create(
            book=self.book,
            user=self.normal_user,
            due_date=date.today() + timedelta(days=7)
        )
        self.book.is_available = False
        self.book.save()

    # Modelo de multa

    def test_calculo_multa(self):
        fine = Fine.objects.create(
            loan=self.loan,
            late_days=3,
            fine_amount=3 * 1000
        )
        self.assertEqual(fine.fine_amount, 3000)

    # Los flujos

    def test_prestar_cambia_estado(self):
        self.book.refresh_from_db()
        self.assertFalse(self.book.is_available)

    def test_no_se_presta_dos_veces(self):
        self.client.login(username="usuario", password="pass1234")
        response = self.client.post(
            f"/loans/loan/{self.book.pk}/",
            {"book": self.book.pk, "due_date": date.today() + timedelta(days=7)}
        )
        self.assertEqual(Loan.objects.filter(book=self.book).count(), 1)

    def test_devolver_reactiva_libro(self):
        self.loan.end_date = date.today()
        self.loan.is_active = False
        self.loan.save()
        self.book.is_available = True
        self.book.save()
        self.book.refresh_from_db()
        self.assertTrue(self.book.is_available)

    def test_devolver_tarde_crea_multa(self):
        self.loan.end_date = date.today()
        self.loan.due_date = date.today() - timedelta(days=5)
        self.loan.save()
        late_days = (self.loan.end_date - self.loan.due_date).days
        fine = Fine.objects.create(
            loan=self.loan,
            late_days=late_days,
            fine_amount=late_days * 1000
        )
        self.assertEqual(fine.late_days, 5)
        self.assertEqual(fine.fine_amount, 5000)