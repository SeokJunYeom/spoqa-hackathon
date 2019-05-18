from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, user_id, nickname, password=None):
        user = self.model(
            user_id=user_id,
            nickname=nickname,
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, user_id, nickname, password=None):
        user = self.create_user(
            user_id=user_id,
            nickname=nickname,
            password=password,
        )

        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(
        verbose_name=_('사용자 아이디'),
        max_length=30,
        unique=True,
    )
    nickname = models.CharField(
        verbose_name=_('닉네임'),
        max_length=30,
    )
    is_active = models.BooleanField(
        verbose_name=_('계정 유효한지'),
        default=True,
    )
    to_do = models.ManyToManyField(
        verbose_name=_('히스토리'),
        to='todo.ToDoText',
        related_name='users',
        through='History',
    )

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['nickname']

    objects = UserManager()

    class Meta:
        verbose_name = _('사용자')
        verbose_name_plural = _('사용자 목록')
        db_table = 'user'

    def __str__(self):
        return self.user_id

    @property
    def is_staff(self):
        return self.is_superuser


class History(models.Model):
    to_do = models.ForeignKey(
        verbose_name=_('to do'),
        to='todo.ToDoText',
        related_name='history',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name=_('사용자'),
        to=settings.AUTH_USER_MODEL,
        related_name='history',
        on_delete=models.CASCADE
    )
    is_done = models.BooleanField(
        verbose_name=_('마쳤냐'),
        default=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_('수정 날짜'),
        auto_now=True,
    )

    class Meta:
        verbose_name = _('히스토리')
        verbose_name_plural = _('히스토리')
        db_table = 'history'
        unique_together = ('to_do', 'user')


class Feed(models.Model):
    img = models.FileField(
        upload_to='image/',
    )
    content = models.TextField(
        blank=True
    )
    to_do = models.ForeignKey(
        to='todo.ToDoText',
        related_name='feed',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='feeds',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
