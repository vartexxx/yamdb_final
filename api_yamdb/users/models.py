from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USERS_ROLES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Пользовательская роль',
        max_length=max(len(role) for role, none_ in USERS_ROLES),
        choices=USERS_ROLES,
        default=USER,
    )
    email = models.EmailField('Email пользователя', unique=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
        unique_together = ('email', 'username')
        indexes = [
            models.Index(fields=['role', ], name='role_idx'),
        ]

    def __str__(self):
        return self.username
