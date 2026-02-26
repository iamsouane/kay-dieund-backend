from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash
from .models import User
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    ChangePasswordSerializer
)

class RegisterView(generics.CreateAPIView):
    """Vue pour l'inscription"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Génère les tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Inscription réussie !"
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """Vue pour la connexion"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Connexion réussie !"
        })

class LogoutView(APIView):
    """Vue pour la déconnexion"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Déconnexion réussie."})
        except Exception:
            return Response(
                {"error": "Token invalide ou manquant."},
                status=status.HTTP_400_BAD_REQUEST
            )

class ProfileView(generics.RetrieveUpdateAPIView):
    """Vue pour consulter et modifier le profil"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            "user": serializer.data,
            "message": "Profil mis à jour avec succès !"
        })

class ChangePasswordView(APIView):
    """Vue pour changer le mot de passe"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Vérifie l'ancien mot de passe
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"old_password": "Ancien mot de passe incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Change le mot de passe
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Garde la session active
        update_session_auth_hash(request, user)
        
        return Response({"message": "Mot de passe changé avec succès !"})