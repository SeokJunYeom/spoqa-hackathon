import base64

from django.contrib.auth import get_user_model, logout
from django.contrib.sessions.models import Session

from rest_framework.generics import GenericAPIView, mixins
from rest_framework.response import Response

from .serializers import UserSerializer, RegistrationSerializer, LoginSerializer


User = get_user_model()


class RegistrationView(GenericAPIView, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request):
        return self.create(request)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = UserSerializer(user)

        return Response(user_serializer.data)


class IsLoginView(GenericAPIView):

    def get(self, request):
        user_id = request.query_params.get('user_id')

        try:
            hash = User.objects.get(user_id=user_id).get_session_auth_hash()

        except User.DoesNotExist:
            return Response({'is_login': False})

        for session_data in Session.objects.values_list('session_data', flat=True):
            data = base64.b64decode(session_data)

            if hash in data.decode('utf-8'):
                return Response({'is_login': True})

        return Response({'is_login': False})


class LogoutView(GenericAPIView):

    def get(self, request):
        user_id = request.query_params.get('user_id')

        try:
            hash = User.objects.get(user_id=user_id).get_session_auth_hash()

        except User.DoesNotExist:
            pass

        for session in Session.objects.all():
            data = base64.b64decode(session.session_data)

            if hash in data.decode('utf-8'):
                session.delete()

        logout(request)

        return Response({'message': 'success'})
