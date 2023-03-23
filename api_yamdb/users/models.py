from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from api.utils import send_email

from .constants import ADMIN, MODERATOR, PASSWORD_LENGTH, USER
from .validators import validate_me


class YamdbUserManager(UserManager):
    def create_superuser(
        self, username, email=None, password=None, **extra_fields
    ):
        user = super().create_superuser(
            username, email, password, **extra_fields
        )
        user.role = ADMIN
        user.save(using=self._db)
        send_email(user)
        return user


class User(AbstractUser):
    CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    username_validator = UnicodeUsernameValidator()
    objects = YamdbUserManager()
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=CHOICES,
        default=USER,
    )
    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True,
        error_messages={
            'unique': _("Такой email уже используется."),
        },
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Обязательно к заполнению.'
            ' <=150 символов. Только буквы, цифры и @/./+/-/_.'
        ),
        validators=(username_validator, validate_me),
        error_messages={
            'unique': _("Это имя занято."),
        },
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    def is_admin(self):
        return self.role == ADMIN

    def is_moderator(self):
        return self.role in (MODERATOR, ADMIN)

    def save(self, *args, **kwargs):
        if not self.password:
            self.password = get_random_string(PASSWORD_LENGTH)

        super().save(*args, **kwargs)
