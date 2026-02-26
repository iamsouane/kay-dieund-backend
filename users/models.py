from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    """Modèle utilisateur personnalisé"""
    
    # Champs supplémentaires
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Le numéro de téléphone doit être au format: '+221 77 123 45 67'."
    )
    phone = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True,
        verbose_name="Téléphone"
    )
    
    # Adresse de livraison par défaut
    address = models.TextField(
        blank=True,
        verbose_name="Adresse"
    )
    city = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="Ville"
    )
    
    # Date de naissance (optionnel)
    birth_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Date de naissance"
    )
    
    # Avatar
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        verbose_name="Photo de profil"
    )
    
    # Booléens
    email_verified = models.BooleanField(
        default=False,
        verbose_name="Email vérifié"
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} - {self.get_full_name()}"