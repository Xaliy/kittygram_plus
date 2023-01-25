from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response


# from django.shortcuts import get_object_or_404

from .models import Cat, Owner
from .serializers import CatSerializer, CatListSerializer, OwnerSerializer
from .serializers import CustomUserSerializer


# Опишем собственный базовый класс вьюсета: он будет создавать экземпляр
#  объекта и получать экземпляр объекта; назовём его CreateRetrieveViewSet.
class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    # В теле класса никакой код не нужен! Пустячок, а приятно.
    pass


class CustomUserViewSet(UserViewSet):
    pass


# Опишем вьюсет LightCatViewSet, унаследованный от CreateRetrieveViewSet.
# Зарегистрируем этот вьюсет в роутере:
class LightCatViewSet(CreateRetrieveViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    # Пишем метод, а в декораторе разрешим работу со списком объектов
    # и переопределим URL на более презентабельный
    @action(detail=False, url_path='recent-white-cats')
    def recent_white_cats(self, request):
        # Нужны только последние пять котиков белого цвета
        cats = Cat.objects.filter(color='White')[:5]
        # Передадим queryset cats сериализатору
        # и разрешим работу со списком объектов
        serializer = self.get_serializer(cats, many=True)
        return Response(serializer.data)

    # урок 12
    # т.к добавили новый сериализатор теперь добавляем метод
    # во вьюсет стандартный метод get_serializer_class:
    def get_serializer_class(self):
        # Если запрошенное действие (action)
        # — получение списка объектов ('list')
        if self.action == 'list':
            # ...то применяем CatListSerializer
            return CatListSerializer
        # А если запрошенное действие — не 'list', применяем CatSerializer
        return CatSerializer


# # а можно так??? или это продолжение?
# # В тех случаях, когда нужно получить больше контроля
# #  и возможностей что-то «подкрутить» во вьюсетах, можно наследоваться
#  от базового класса ViewSet.
# #  Именно от него наследуется, например, класс ModelViewSet.
# # Похоже на то, как мы работали в APIView,
# #  с той разницей, что здесь присутствуют поля queryset и serializer.

# class CatViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Cat.objects.all()
#         serializer = CatSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = Cat.objects.all()
#         cat = get_object_or_404(queryset, pk=pk)
#         serializer = CatSerializer(cat)
#         return Response(serializer.data)

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
