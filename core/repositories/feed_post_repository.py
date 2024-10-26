from core.models.feed_post_model import FeedPost
from core.models.user_model import User
from core.repositories.user_following_repository import UserFollowingRepository
from core.repositories.programming_group_repository import ProgrammingGroupRepository

class FeedPostRepository:
    @staticmethod
    def filter_posts(user, group_titles=None, difficulty_levels=None, interest_areas=None):
        # Inicie a consulta de posts
        posts = FeedPost.objects.all()

        if group_titles:
            # Filtrar posts com base nos títulos dos grupos
            posts = posts.filter(group__title__in=group_titles)

        if difficulty_levels:
            # Filtrar posts com base nos níveis de dificuldade
            posts = posts.filter(difficulty_level__in=difficulty_levels)

        if interest_areas:
            # Filtrar posts com base nas áreas de interesse
            posts = posts.filter(interest_area__name__in=interest_areas)  # Use 'name' se 'Interest' tiver um campo de nome

        return posts

    @staticmethod
    def clear_filters(user: User):
        """
        Retorna todos os posts do usuário sem aplicar filtros.

        :param user: O usuário cujo feed de posts será retornado.
        :return: QuerySet de todos os posts.
        """
        # Obtém todos os posts sem aplicar filtros
        return FeedPost.objects.all()

    @staticmethod
    def get_feed_posts(user: User, groups=None, difficulty_levels=None, interest_areas=None):
        """
        Retorna os posts do feed para o usuário com base nos filtros fornecidos.

        :param user: O usuário cujo feed de posts será retornado.
        :param groups: Lista de grupos pelos quais filtrar os posts (opcional).
        :param difficulty_levels: Lista de níveis de dificuldade dos posts (opcional).
        :param interest_areas: Lista de áreas de interesse dos posts (opcional).
        :return: QuerySet de posts do feed filtrados.
        """
        if groups or difficulty_levels or interest_areas:
            # Chama o método de filtragem para obter os posts
            return FeedPostRepository.filter_posts(user, groups, difficulty_levels, interest_areas)
        else:
            # Se não houver filtros, chama o método clear_filters para obter todos os posts
            return FeedPostRepository.clear_filters(user)