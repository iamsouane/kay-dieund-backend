from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icône")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    price = models.IntegerField(verbose_name="Prix (FCFA)")  # Changé en IntegerField pour FCFA
    description = models.TextField(verbose_name="Description")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name="Catégorie"
    )
    image = models.ImageField(
        upload_to='products/', 
        blank=True, 
        null=True,
        verbose_name="Image"
    )
    image_url = models.URLField(
        max_length=500, 
        blank=True,
        verbose_name="URL de l'image"
    )
    rating_rate = models.FloatField(
        default=4.5,
        verbose_name="Note moyenne"
    )
    rating_count = models.IntegerField(
        default=0,
        verbose_name="Nombre d'avis"
    )
    stock = models.IntegerField(
        default=10,
        verbose_name="Stock disponible"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']
    
    def price_formatted(self):
        """Retourne le prix formaté en FCFA"""
        return f"{self.price:,} FCFA".replace(",", " ")
