from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('migrate/', views.run_migrations_view),
    path('import-products/', views.import_products_view),
    path('create-admin/', views.create_superuser_view),
]
