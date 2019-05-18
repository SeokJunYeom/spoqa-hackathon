import base64

from django.db.models import Count
from django.contrib.auth import get_user_model, logout
from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView, mixins
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action

from todo.models import Recommend
from .models import History, Feed
from .serializers import (
    UserSerializer, RegistrationSerializer, LoginSerializer, UserToDoSerializer, FeedSerializer
)
from .paginations import ListPagination


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


class UserToDoView(APIView):
    serializer_class = UserToDoSerializer

    def get(self, request, id):
        try:
            user = User.objects.get(id=self.kwargs['id'])

        except User.DoesNotExist:
            return Response({'message': '존재 하지 않는 사용자 입니다.'}, status=status.HTTP_404_NOT_FOUND)

        recommend = Recommend.objects.first().to_do_list.all()
        history = user.to_do.all()

        ids = history.values_list('id', flat=True)

        recommend = recommend.exclude(id__in=ids)

        for rec in recommend:

            tmp = History.objects.filter(user=user, to_do=rec)

            if tmp.exists():
                pass

            else:
                History.objects.create(user=user, to_do=rec, is_done=False)

        queryset = user.history.order_by('is_done', '-updated_at')

        context = {
            'request': request,
        }

        paginator = ListPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request, view=None)
        serializer = self.serializer_class(paginated_queryset, many=True, context=context)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request, id):

        try:
            user = User.objects.get(id=self.kwargs['id'])

        except User.DoesNotExist:
            return Response({'message': '존재 하지 않는 사용자 입니다.'}, status=status.HTTP_404_NOT_FOUND)

        to_do_id = request.data['to_do']

        tmp = History.objects.filter(user=user, to_do_id=to_do_id)
        if tmp.exists():
            his = tmp[0]
            his.is_done = True
            his.save()

        else:
            History.objects.create(user=user, to_do_id=to_do_id, is_done=True)

        return Response({'message': 'success'})


class FeedView(ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    parser_classes = (MultiPartParser,)


class UserPostView(ModelViewSet):
    queryset = User.objects.all()
    serializer_classes = UserSerializer

    @action(detail=True, methods=['get'])
    def posts(self, reuqest, pk):
        user = self.get_object()
        queryset = user.feeds
        serializer = FeedSerializer(queryset, many=True)

        return Response(serializer.data)


class RankView(APIView):

    def get(self, request):
        user_id = request.query_params.get('user_id')
        queryset = User.objects.annotate(count=Count('feeds')).values('nickname', 'count').order_by('-count')
        my = queryset.get(id=user_id)

        return Response({
            'my': my,
            'all': queryset
        })
