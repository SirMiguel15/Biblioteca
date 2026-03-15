from django.urls import path
from . import views

urlpatterns = [
    path("loan/<int:book_pk>/", views.LoanCreateView.as_view(), name="loan-create"),
    path("return/<int:pk>/", views.LoanReturnView.as_view(), name="loan-return"),
    path("my-loans/", views.MyLoansView.as_view(), name="my-loans"),
    path("all-loans/", views.AllLoansView.as_view(), name="all-loans"),
]

