from django.contrib.auth import get_user_model, authenticate, login
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .models import History, Feed


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'user_id', 'nickname', 'is_active',)


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'user_id', 'nickname', 'password', 'is_active')
        extra_kwargs = {
            'is_active': {
                'read_only': True,
            },
            'password': {
                'write_only': True,
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        user = authenticate(user_id=attrs['user_id'], password=attrs['password'])

        if user is None:
            raise serializers.ValidationError(_('일치하는 게정이 없습니다.'))

        request = self.context['request']
        login(request, user)

        attrs['user'] = user

        return attrs


class UserToDoSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = ('is_done', 'text', 'to_do', 'created_at', 'updated_at')

    def get_text(self, obj):
        return obj.to_do.text

    def get_created_at(self, obj):
        return obj.to_do.created_at


class FeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feed
        fields = '__all__'
        extra_kwargs = {
            'created_at': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        history = History.objects.get(user_id=validated_data['user'], to_do_id=validated_data['to_do'])
        history.is_done = True
        history.save()
        return super().create(validated_data)
 
