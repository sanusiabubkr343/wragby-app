from rest_framework import viewsets
from  rest_framework.viewsets import ModelViewSet

from user.models import User
from user.serializers import UserSerializer, CreateUserSerializer


class UserViewSets(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ['get', 'post','put']

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer

