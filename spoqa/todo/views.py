from rest_framework.generics import GenericAPIView, mixins

from .models import Recommend
from .serializers import ToDoTextSerializer


class RecommendView(GenericAPIView, mixins.ListModelMixin):
    #queryset = Recommend.objects.first().to_do_list.all()
    serializer_class = ToDoTextSerializer

    def get(self, request):
        return self.list(request)
