from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Author, Book

class CatalogTestCase(TestCase):

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

    # Modelos

    def test_creacion_valida_book(self):
        self.assertEqual(self.book.title, "Cien años de soledad")
        self.assertEqual(self.book.author, self.author)

    def test_isbn_invalido_duplicado(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title="Otro libro",
                author=self.author,
                isbn="1234567890123"
            )

    def test_disponibilidad_por_defecto(self):
        self.assertTrue(self.book.is_available)

    # Visitas Publicas

    def test_catalogo_responde_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_busqueda_filtra_por_titulo(self):
        response = self.client.get("/", {"q": "cien años"})
        self.assertContains(response, "Cien años de soledad")

    def test_busqueda_filtra_por_autor(self):
        response = self.client.get("/", {"q": "gabriel"})
        self.assertContains(response, "Cien años de soledad")

    # Acceso

    def test_visitante_bloqueado_crear_libro(self):
        response = self.client.get("/books/new/")
        self.assertEqual(response.status_code, 302)

    def test_autenticado_no_staff_bloqueado(self):
        self.client.login(username="usuario", password="pass1234")
        response = self.client.get("/books/new/")
        self.assertEqual(response.status_code, 403)

    def test_staff_puede_acceder_crear_libro(self):
        self.client.login(username="staff", password="pass1234")
        response = self.client.get("/books/new/")
        self.assertEqual(response.status_code, 200)


