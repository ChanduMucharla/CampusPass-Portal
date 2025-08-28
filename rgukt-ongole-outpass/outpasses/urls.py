
from django.urls import path
from . import views

urlpatterns = [
    path('verify/<str:token>/', views.verify_outpass, name='verify_outpass'),
    path('apply/', views.apply_outpass, name='apply_outpass'),
    path('my/', views.my_outpasses, name='my_outpasses'),
    path('manage/', views.manage_outpasses, name='manage_outpasses'),
    path('approve/<int:pk>/', views.approve_outpass, name='approve_outpass'),
    path('reject/<int:pk>/', views.reject_outpass, name='reject_outpass'),
    path('qr/<int:pk>/', views.outpass_qr, name='outpass_qr'),
]
