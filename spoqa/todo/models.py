from django.db import models
from django.utils.translation import ugettext_lazy as _

from account.models import History


class ToDoKeyword(models.Model):
    TYPE_CHOICES = (
        ('where', '어디서'),
        ('who', '누구와'),
        ('what', '무엇을'),
        ('how', '어떻게'),
    )
    type = models.CharField(
        verbose_name=_('타입'),
        max_length=5,
        choices=TYPE_CHOICES,
    )
    text = models.TextField(
        verbose_name=_('텍스트'),
    )

    class Meta:
        verbose_name = _('to do 키워드')
        verbose_name_plural = _('to do 키워드 목록')
        unique_together = ('type', 'text')
        db_table = 'to_do_keyword'

    def __str__(self):
        return self.text


class ToDoTextManager(models.Manager):

    def make(self, count):
        where_list = ToDoKeyword.objects.filter(type='where').order_by('?')[:count]
        who_list = ToDoKeyword.objects.filter(type='who').order_by('?')[:count]
        what_list = ToDoKeyword.objects.filter(type='what').order_by('?')[:count]
        how_list = ToDoKeyword.objects.filter(type='how').order_by('?')[:count]

        to_do_list = []

        for i in range(count):
            text = f'{where_list[0].text} {who_list[0].text} {how_list[0].text} {what_list[0].text}'
            to_do_list.append(self.model.objects.create(text=text))

        return to_do_list


class ToDoText(models.Model):
    text = models.TextField(
        verbose_name=_('to do'),
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_('생성 날짜'),
        auto_now_add=True,
    )

    objects = ToDoTextManager()

    class Meta:
        verbose_name = _('to do text')
        verbose_name_plural = _('to do text')
        db_table = 'to_do_text'
        ordering = ['-created_at']

    def __str__(self):
        return self.text


class RecommendManager(models.Manager):

    def make_list(self, count):
        History.objects.filter(is_done=False).delete()
        recommend = self.model.objects.first() or self.model.objects.create()
        recommend.to_do_list.clear()
        recommend.to_do_list.add(*ToDoText.objects.make(count))


class Recommend(models.Model):
    to_do_list = models.ManyToManyField(
        verbose_name=_('추천 to do 목록'),
        to='ToDoText',
        related_name='recommend',
    )

    objects = RecommendManager()

    class Meta:
        verbose_name = _('추천 to do')
        verbose_name_plural = _('추천 to do')
        db_table = 'recommend'

    def __str__(self):
        return '추천 목록'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
