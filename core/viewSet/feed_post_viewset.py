from rest_framework import viewsets, status
from rest_framework.response import Response
from core.services.feed_post_service import FeedPostRepository  # Ajuste conforme necessário
from core.serializers.feed_post_serialiazer import FeedPostSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication 
from core.models.feed_post_model import FeedPost

class FeedPostViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = FeedPost.objects.all()
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='group_titles', type=str, location=OpenApiParameter.QUERY, description='Filtrar por títulos de grupos.'),
            OpenApiParameter(name='difficulty_levels', type=str, location=OpenApiParameter.QUERY, description='Filtrar por níveis de dificuldade.'),  
            OpenApiParameter(name='interest_areas', type=str, location=OpenApiParameter.QUERY, description='Filtrar por áreas de interesse.')
        ],
        responses={200: FeedPostSerializer(many=True)},
    )
    
    def list(self, request, *args, **kwargs):
        user = request.user  # Supondo que você tenha um usuário autenticado

        group_titles = request.query_params.getlist('group_titles')  # Certifique-se de que o nome do parâmetro está correto
        difficulty_levels = request.query_params.getlist('difficulty_levels')
        interest_areas = request.query_params.getlist('interest_areas')

        # Converter níveis de dificuldade para inteiros, se necessário
        difficulty_levels = [int(level) for level in difficulty_levels if level.isdigit()]

        # Converter áreas de interesse para uma lista de strings, se necessário
        # Aqui, como as áreas de interesse já são strings, não há necessidade de conversão
        interest_areas = [area for area in interest_areas if area]

        # Filtrar os posts com base nos parâmetros
        posts = FeedPostRepository.filter_posts(user, group_titles, difficulty_levels, interest_areas)

        # Serializar os posts e retornar a resposta
        serializer = FeedPostSerializer(posts, many=True)
        return Response(serializer.data)
