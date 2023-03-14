from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import get_object_or_404
from reviews.models import Category, Comment, Genre, Review, Title

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserGetOrPatchSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=140, regex=r'^[\w.@+-]+\Z', required=True)
    email = serializers.EmailField(max_length=254, required=True)

    def validate(self, attr):
        username = attr['username']
        email = attr['email']
        if 'me' == username:
            raise serializers.ValidationError(
                f'Извините, имя пользователя "{username}" недоступно.'
            )
        if User.objects.filter(username=username, email=email).exists():
            return attr
        return attr

    def validate_email(self, email):
        req_username = self.initial_data.get('username')
        if User.objects.filter(email=email).exists():
            user_by_email = User.objects.get(email=email).username
            if req_username != user_by_email:
                raise serializers.ValidationError(
                    f'Извините, email: {email} недоступно.')
        return email

    def validate_username(self, username):
        req_email = self.initial_data['email']
        if User.objects.filter(username=username).exists():
            email = User.objects.get(username=username).email
            if req_email != email:
                raise serializers.ValidationError(
                    f'Извините, имя пользователя {username} недоступно.')
        return username

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenForUserSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, attr):
        username = attr['username']
        if not User.objects.filter(username=username).exists():
            raise NotFound(
                f'Извините, пользователя {username} не существует.')
        return attr


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if title.reviews.select_related('title').filter(author=author):
                raise ValidationError('Только один отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        lookup_field = 'slug'
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        lookup_field = 'slug'
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        read_only_fields = ('id',)
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category',
        )

    def get_rating(self, obj):
        obj = obj.reviews.all().aggregate(rating=Avg('score'))
        return obj['rating']


class TitleWriteSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.now().year)
        ]
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        many=True,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
