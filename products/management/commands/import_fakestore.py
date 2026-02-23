import requests
from django.core.management.base import BaseCommand
from products.models import Product, Category

class Command(BaseCommand):
    help = 'Import products from FakeStore API'

    def handle(self, *args, **kwargs):
        self.stdout.write('🔄 Importation des produits depuis FakeStoreAPI...')
        
        # Taux de conversion : 1 USD = 600 FCFA
        USD_TO_FCFA = 600
        
        # Catégories avec noms en français
        categories = {
            "men's clothing": {
                "name": "Vêtements Homme",
                "slug": "men-s-clothing"
            },
            "women's clothing": {
                "name": "Vêtements Femme",
                "slug": "women-s-clothing"
            },
            "jewelery": {
                "name": "Bijoux",
                "slug": "jewelery"
            },
            "electronics": {
                "name": "Électronique",
                "slug": "electronics"
            }
        }
        
        # Créer les catégories
        for old_slug, cat_data in categories.items():
            category, created = Category.objects.update_or_create(
                slug=cat_data["slug"],
                defaults={'name': cat_data["name"]}
            )
            if created:
                self.stdout.write(f'  ✅ Catégorie créée: {cat_data["name"]}')
            else:
                self.stdout.write(f'  ℹ️ Catégorie mise à jour: {cat_data["name"]}')
        
        # Importer les produits
        self.stdout.write('📦 Récupération des produits...')
        response = requests.get('https://fakestoreapi.com/products')
        
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('❌ Erreur de connexion à FakeStoreAPI'))
            return
        
        products = response.json()
        self.stdout.write(f'  ✅ {len(products)} produits trouvés')
        
        # Compteurs
        created_count = 0
        updated_count = 0
        
        for item in products:
            # Récupérer la catégorie avec le nouveau slug
            category_slug = categories[item['category']]["slug"]
            category = Category.objects.get(slug=category_slug)
            
            # Convertir le prix en FCFA (arrondi à l'entier)
            price_fcfa = int(float(item['price']) * USD_TO_FCFA)
            
            product, created = Product.objects.update_or_create(
                id=item['id'],
                defaults={
                    'title': item['title'],
                    'price': price_fcfa,  # Prix en FCFA
                    'description': item['description'],
                    'category': category,
                    'image_url': item['image'],
                    'rating_rate': item['rating']['rate'],
                    'rating_count': item['rating']['count'],
                    'stock': 10
                }
            )
            
            if created:
                created_count += 1
            else:
                updated_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Import terminé !\n'
            f'   {created_count} produits créés\n'
            f'   {updated_count} produits mis à jour\n'
            f'   💰 Taux de conversion: 1 USD = {USD_TO_FCFA} FCFA'
        ))
