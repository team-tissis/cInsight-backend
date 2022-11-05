from django.db.models import QuerySet
from django_filters import rest_framework as filters
from rest_framework import viewsets, status

from api.filters import CustomPagination, NoPagination
from api.models import Comment, CustomeUser
from api.serializers.comment_serializer import CommentSerializer

from rest_framework.decorators import action
from api.utils import HttpMethod
from django.db import transaction
from rest_framework.request import Request
from rest_framework.response import Response

class CommentFilter(filters.FilterSet):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Comment] = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_class = CommentFilter
    pagination_class = CustomPagination

    @transaction.atomic
    @action(detail=False, methods=[HttpMethod.PUT.name])
    def favo(self, request: Request, *args, **kwargs):
        commentId = request.data.get("id")
        if commentId is None:
            return Response({"user": None, "message": "アカウントアドレスが指定されていません"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                comment = Comment.objects.get(id=commentId)    
                if comment.favo is None:
                    comment.favo = 0
                comment.favo += 1
                comment.save()
                return Response({"message": "コメントにいいねしました"}, status=status.HTTP_200_OK)
            except:
                return Response({"message": "Commentが見つかりませんでした"}, status=status.HTTP_404_NOT_FOUND)
        
        # account_address = request.query_params.get("")
        # if account_address is None:
        #     return Response({"user": None, "message": "アカウントアドレスが指定されていません"}, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     users = CustomeUser.objects.filter(eoa=account_address)
        #     if users.count() == 0:
        #         return Response({"user": None, "message": "Userが見つかりませんでした"}, status=status.HTTP_404_NOT_FOUND)
        #     else:
        #         user = user.first()
        #         serializer = UserSerializer(user)
        #         return Response({"user": serializer.data}, status=status.HTTP_200_OK)
