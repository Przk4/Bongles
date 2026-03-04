from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import CustomUser, UserProfile
from apps.users.serializers import (
    CustomUserSerializer, UserDetailSerializer, UserProfileSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return CustomUserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Registrar un nuevo usuario."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': CustomUserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Login de usuario."""
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': CustomUserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response(
            {'detail': 'Credenciales inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Obtener datos del usuario autenticado."""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request, pk=None):
        """Actualizar perfil del usuario."""
        user = self.get_object()
        self.check_object_permissions(request, user)
        
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
