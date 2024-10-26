from rest_framework import serializers
from core.models.feed_post_model import FeedPost
from core.models.user_model import User
from core.models.programming_group_model import ProgrammingGroup

class FeedPostSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='name', queryset=ProgrammingGroup.objects.all())
    author = serializers.SlugRelatedField(slug_field='name', read_only=True)  # Exibe o nome do autor

    class Meta:
        model = FeedPost
        fields = ['id', 'title', 'content', 'difficulty_level', 'interest_area', 'group', 'author', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']  # Campos somente leitura

