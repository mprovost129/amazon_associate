from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('go/<int:pk>/', views.ProductRedirectView.as_view(), name='redirect'),
]
