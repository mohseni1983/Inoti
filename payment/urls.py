from django.urls import path

from payment import views

urlpatterns=[
    path('<str:payid>/',views.payment),
    path('',views.notfound)
]