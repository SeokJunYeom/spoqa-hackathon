from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, username, nickname, password=None):
        user = self.model(
            username=username,
            nickname=nickname,
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, nickname, password=None):
        user = self.create_user(
            username=username,
            nickname=nickname,
            password=password,
        )

        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name=_('사용자명'),
        max_length=30,
    )
    nickname = models.CharField(
        verbose_name=_('닉네임'),
        max_length=30,
        unique=True,
    )
    is_active = models.BooleanField(
        verbose_name=_('계정 유효한지'),
        default=True,
    )

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        verbose_name = _('사용자')
        verbose_name_plural = _('사용자 목록')
        db_table = 'user'

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser
