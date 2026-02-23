from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth.models import User
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# Vues API existantes
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'title', 'created_at']

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

def run_migrations_view(request):
    """
    Vue temporaire pour exécuter les migrations.
    À APPELER EN PREMIER.
    """
    try:
        from django.core.management import call_command
        call_command('migrate')
        return HttpResponse("""
            <h1 style='color: green;'>✅ Migrations exécutées avec succès !</h1>
            <p>Les tables ont été créées.</p>
            <p>Vous pouvez maintenant :</p>
            <ol>
                <li><a href='/api/create-admin/'>Créer un superutilisateur</a></li>
                <li><a href='/api/import-products/'>Importer les produits</a></li>
            </ol>
        """)
    except Exception as e:
        return HttpResponse(f"""
            <h1 style='color: red;'>❌ Erreur</h1>
            <p>{str(e)}</p>
        """)

# Vues temporaires pour l'initialisation sur Render
def import_products_view(request):
    """
    Vue temporaire pour importer les produits depuis FakeStoreAPI.
    À SUPPRIMER après utilisation.
    """
    try:
        call_command('import_fakestore')
        return HttpResponse("""
            <h1 style='color: green;'>✅ Succès !</h1>
            <p>Les produits ont été importés avec succès depuis FakeStoreAPI.</p>
            <p>Vous pouvez maintenant accéder à :</p>
            <ul>
                <li><a href='/api/products/'>/api/products/</a> - Liste des produits</li>
                <li><a href='/admin/'>/admin/</a> - Interface d'administration</li>
            </ul>
            <p><small>N'oubliez pas de supprimer cette vue après utilisation.</small></p>
        """)
    except Exception as e:
        return HttpResponse(f"""
            <h1 style='color: red;'>❌ Erreur</h1>
            <p>{str(e)}</p>
        """)

def create_superuser_view(request):
    """
    Vue temporaire pour créer un superutilisateur par défaut.
    À SUPPRIMER après utilisation.
    """
    try:
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            return HttpResponse("""
                <h1 style='color: green;'>✅ Superutilisateur créé !</h1>
                <p><strong>Nom d'utilisateur:</strong> admin</p>
                <p><strong>Mot de passe:</strong> admin123</p>
                <p><strong>Email:</strong> admin@example.com</p>
                <p>Vous pouvez maintenant vous connecter à <a href='/admin/'>l'interface d'administration</a>.</p>
                <p><small>⚠️ Changez ce mot de passe après votre première connexion !</small></p>
                <p><small>N'oubliez pas de supprimer cette vue après utilisation.</small></p>
            """)
        else:
            users = User.objects.filter(is_superuser=True)
            user_list = "<br>".join([f"- {u.username} ({u.email})" for u in users])
            return HttpResponse(f"""
                <h1 style='color: orange;'>ℹ️ Superutilisateur existant</h1>
                <p>Un superutilisateur existe déjà :</p>
                <p>{user_list}</p>
                <p>Connectez-vous à <a href='/admin/'>l'interface d'administration</a>.</p>
            """)
    except Exception as e:
        return HttpResponse(f"""
            <h1 style='color: red;'>❌ Erreur</h1>
            <p>{str(e)}</p>
        """)
