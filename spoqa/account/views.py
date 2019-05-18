from django.contrib.auth import get_user_model, logout

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

        if request.user and request.user.is_authenticated:
            return Response({'is_login': True})

        return Response({'is_login': False})


class LogoutView(GenericAPIView):

    def get(self, request):
        logout(request)

        return Response({'message': 'success'})