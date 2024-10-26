from core.models.feed_post_model import FeedPost
from core.models.user_model import User
from core.repositories.feed_post_repository import FeedPostRepository

class PostService:
    
    @staticmethod
    def get_feed_for_user(user: User, groups=None, difficulty_levels=None, interest_areas=None):
        """
        Retorna o feed de posts para o usuário com base nos filtros escolhidos.
        """
        # Chama o repositório para obter os posts filtrados
        posts = FeedPostRepository.filter_posts(user, groups, difficulty_levels, interest_areas)
        return posts
    
    @staticmethod
    def clear_filters(user: User):
        """
        Retorna todos os posts dos grupos em que o usuário participa, sem aplicar filtros.
        :param user: O usuário que está limpando os filtros.
        :return: QuerySet de todos os posts dos grupos do usuário.
        """
        # Chama o repositório para obter os posts sem filtros
        posts = FeedPostRepository.filter_posts(user)
        return posts