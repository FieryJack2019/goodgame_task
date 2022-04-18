from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, ListAPIView, RetrieveAPIView
from .models import UserProfile, Game, Category
from .serializers import UserProfileSerializer, GameSerializer, CategorySerializer
from rest_framework.response import Response


class UserList(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        gameId = self.kwargs['gameId']
        return UserProfile.objects.filter(mainGame=Game.objects.get(pk=gameId), isActive=True)


class UserCreate(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserDetail(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs.keys():
            return Response(UserProfileSerializer(UserProfile.objects.get(pk=kwargs['pk'])).data)
        else:
            return Response(UserProfileSerializer(UserProfile.objects.filter(telegramID=request.GET.get('telegramID')).first()).data)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class GameList(ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_queryset(self):
        categoryId = self.kwargs['categoryId']
        return Game.objects.filter(category=Category.objects.get(pk=categoryId))


class GameDetail(RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer