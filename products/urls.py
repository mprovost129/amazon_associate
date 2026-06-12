from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('products/', views.ProductSearchView.as_view(), name='search'),
    path('products/import/', views.ProductImportView.as_view(), name='import'),
    path('products/export/', views.ProductExportView.as_view(), name='export'),
    path('go/<int:pk>/', views.ProductRedirectView.as_view(), name='redirect'),
    path('collections/', views.CollectionListView.as_view(), name='collection_list'),
    path('collections/<slug:slug>/', views.CollectionDetailView.as_view(), name='collection_detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
    path('p/<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
]
