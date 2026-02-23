from django.core.management import call_command
from django.http import HttpResponse
from django.urls import path
from django.contrib import admin

# À ajouter temporairement dans products/views.py
def import_products_view(request):
    try:
        call_command('import_fakestore')
        return HttpResponse("✅ Produits importés avec succès !")
    except Exception as e:
        return HttpResponse(f"❌ Erreur: {str(e)}")

def create_superuser_view(request):
    from django.contrib.auth.models import User
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        return HttpResponse("✅ Superutilisateur créé : admin / admin123")
    return HttpResponse("ℹ️ Un superutilisateur existe déjà")
