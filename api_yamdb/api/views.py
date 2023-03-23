from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenViewBase

from api.filters import TitleFilter
from api.mixins import CreateListDestroyViewSet
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             IsOwnerOrStaffOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleCreateSerializer, TitleReadSerializer,
                             TokenObtainSerializer, UserSerializer,
                             UserSignUpSerializer)
from api.utils import send_email
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для Genre."""

    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для Cayegory."""

    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для Title."""

    queryset = (
        Title.objects.all().annotate(Avg('reviews__score')).order_by('id')
    )
    # так как добавили avg - сортировка из модели не работает. без сортировки
    # в запросе выдаются предупреждения в тесте. Может оставить?
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filterset_class = TitleFilter
    filterset_fields = (
        'category',
        'genre',
        'name',
        'year',
    )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer

        return TitleCreateSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для Comment."""

    permission_classes = (IsOwnerOrStaffOrReadOnly,)
    serializer_class = CommentSerializer
    http_method_names = ('get', 'post', 'head', 'patch', 'delete')

    def get_review(self):
        """Возвращает отзыв"""

        return get_object_or_404(
            Review,
            pk=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id"),
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для Review."""

    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrStaffOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


@api_view(['POST'])
def user_sign_up(request):
    serializer = UserSignUpSerializer(data=request.data)

    existing_user = User.objects.filter(
        username=request.data.get('username')
    ).first()
    if existing_user and existing_user.email == request.data.get('email'):
        send_email(existing_user)
        return Response(request.data, status=status.HTTP_200_OK)

    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    send_email(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(TokenViewBase):
    """Вьюсет для Token."""

    serializer_class = TokenObtainSerializer


class UserViewSet(ModelViewSet):
    """Вьюсет для User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    permission_classes = (IsAuthenticated, IsAdmin)
    http_method_names = ('get', 'post', 'head', 'patch', 'delete')

    @action(
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated,),
        detail=False,
        url_path='me',
    )
    def current_user(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop('role', None)
        serializer.update(request.user, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
