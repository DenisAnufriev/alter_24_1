from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from dogs.models import Breed, Dog
from dogs.paginations import CustomPagination
from dogs.serializer import BreedSerializer, DogSerializer, DogDetailSerializer
from users.permissions import IsModer, IsOwner


class DogViewSet(ModelViewSet):
    queryset = Dog.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ("breed",)
    ordering_filters = ("date_born",)
    search_fields = ("name",)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DogDetailSerializer
        return DogSerializer

    def perform_create(self, serializer):
        dog = serializer.save()
        dog.owner = self.request.user
        dog.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()


class BreedCreateAPIView(CreateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (~IsModer, IsAuthenticated)


class BreedListAPIView(ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    pagination_class = CustomPagination


class BreedRetrieveAPIView(RetrieveAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)

    def perform_create(self, serializer):
        breed = serializer.save()
        breed.owner = self.request.user
        breed.save()


class BreedUpdateAPIView(UpdateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)



class BreedDestroyAPIView(DestroyAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)

