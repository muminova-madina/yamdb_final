from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import account_access_token
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class GenreSerializer(ModelSerializer):
    """Сериализатор для Genre."""

    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


class CategorySerializer(ModelSerializer):
    """Сериализатор для Category."""

    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class TitleReadSerializer(ModelSerializer):
    """Сериализатор для Title на чтение."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'rating',
            'genre',
            'category',
        )
        model = Title


class TitleCreateSerializer(ModelSerializer):
    """Сериализатор для Title на создание и изменение."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug', required=False
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=False,
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )
        model = Title


class CommentSerializer(ModelSerializer):
    """Сериализатор для Comment."""

    review = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'review', 'text', 'pub_date', 'author')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для Review."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы уже оставили отзыв.')
        return data

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)


class UserSignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenObtainSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs.get('username'))
        if not account_access_token.check_token(
            user, attrs.get('confirmation_code')
        ):
            raise serializers.ValidationError('Некорректный код подтверждения')
        refresh = RefreshToken.for_user(user)
        data = {'access_token': str(refresh.access_token)}
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
