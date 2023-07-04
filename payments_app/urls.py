from django.urls import path

from .views import success_payment, result_payment

urlpatterns = [
    path('success/', success_payment),
    path('result/', result_payment),
]
