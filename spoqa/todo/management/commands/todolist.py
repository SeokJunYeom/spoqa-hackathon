import os
import json
import codecs

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from todo.models import ToDoKeyword


class Command(BaseCommand):

    def handle(self, *args, **options):

        with codecs.open(os.path.join(settings.BASE_DIR, 'todolist.json'), encoding='utf-8') as f:
            todolist = json.load(f)

        for type, text_list in todolist.items():

            for text in text_list:

                try:
                    ToDoKeyword.objects.create(
                        type=type,
                        text=text
                    )

                except IntegrityError:
                    pass
