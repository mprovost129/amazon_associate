from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('go/<int:pk>/', views.ProductRedirectView.as_view(), name='redirect'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
]
