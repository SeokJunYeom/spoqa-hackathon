from rest_framework import serializers

from .models import ToDoText


class ToDoTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = ToDoText
        fields = '__all__'
