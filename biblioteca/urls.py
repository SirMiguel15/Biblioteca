
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("catalog.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls")),
    path("loans/", include("loans.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]