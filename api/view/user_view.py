from django.db.models import QuerySet
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from api.models import CustomUser
from api.filters import NoPagination
from api.serializers.user_serializer import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from api.utils import HttpMethod
from django.db import transaction
from rest_framework.request import Request


class UserFilter(filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = "__all__"


class UserViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[CustomUser] = CustomUser.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    pagination_class = NoPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(detail=False, methods=[HttpMethod.GET.name])
    def fetch_by_account_address(self, request: Request, *args, **kwargs):
        account_address = request.query_params.get("account_address")
        print("account_address:", account_address)
        if account_address is None:
            return Response({"user": None, "message": "アカウントアドレスが指定されていません"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            users = CustomUser.objects.filter(eoa=account_address)
            if users.count() == 0:
                return Response({"user": None}, status=status.HTTP_404_NOT_FOUND)
            else:
                user = users.first()
                serializer = UserSerializer(user)
                return Response({"user": serializer.data}, status=status.HTTP_200_OK)
