from django.urls import path

from payment import views

urlpatterns=[
    path('verify/', views.verify,name='verify'),

    path('<str:payid>/',views.payment,name='payment-page'),
    path('',views.notfound),

]