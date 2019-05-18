from django.contrib.auth import get_user_model, authenticate, login
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


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

