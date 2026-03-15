# Proyecto de Biblioteca — Django MVT

## Requisitos
- Python 3.x
- pip

## Instalación

### 1. Descarga el repositorio
https://github.com/SirMiguel15/Biblioteca.git

### 2. Crea y activa el entorno virtual
python -m venv venv
venv\Scripts\activate

### 3. Instala dependencias
pip install -r requirements.txt

## Migraciones
python manage.py migrate

## Crear superusuario
python manage.py createsuperuser

## Correr servidor
python manage.py runserver

## Correr tests
python manage.py test

## URLs disponibles

* Catálogo: http://127.0.0.1:8000/
* Detalle de libro: http://127.0.0.1:8000/books/<id>/
* Crear libro (staff): http://127.0.0.1:8000/books/new/
* Mis préstamos: http://127.0.0.1:8000/loans/my-loans/
* Todos los préstamos (staff): http://127.0.0.1:8000/loans/all-loans/
* Login: http://127.0.0.1:8000/accounts/login/
* Admin: http://127.0.0.1:8000/admin/

## Aplicaciones
- **catalog**: gestión de libros y autores
- **loans**: préstamos, devoluciones y multas

## Roles
- **Visitante**: ver catálogo y buscar libros
- **Autenticado**: solicitar préstamos, ver mis préstamos
- **Staff**: CRUD libros, gestionar préstamos, registrar devoluciones
