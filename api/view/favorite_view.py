from django.db.models import QuerySet
from django_filters import rest_framework as filters
from rest_framework import viewsets, status

from api.filters import CustomPagination, NoPagination
from api.models import Lecture, CustomeUser, Favorite
from api.serializers.favorite_serializer import FavoriteSerializer

from rest_framework.decorators import action
from api.utils import HttpMethod
from django.db import transaction
from rest_framework.request import Request
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie

class FavoriteFilter(filters.FilterSet):
    class Meta:
        model = Favorite
        fields = "__all__"

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Favorite] = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    filter_class = FavoriteFilter
    pagination_class = CustomPagination

    @transaction.atomic
    @action(detail=False, methods=[HttpMethod.GET.name])
    def user_favorites(self, request: Request, *args, **kwargs):
        account_address = request.query_params.get("account_address")

        if account_address is None:
            return Response({"message": "いいね取得失敗"}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomeUser.objects.filter(eoa=account_address)
        try:
            # 自分が発行した勉強会を取得
            lectures = Lecture.objects.filter(author=user.get())
            result = []
            for lecture in lectures:
                favorites = Favorite.objects.filter(lecture=lecture, is_synced=False)
                result.append([
                    {"id": favo.id, "volume": favo.vote_weight, "eoa": favo.user.eoa}
                    for favo in favorites
                ])
            result = sum(result, [])
            return Response({"results": result}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "無効なユーザーです"}, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
        lectureId = request.data.get("lecture_id")
        eoa = request.data.get("eoa")
        
        if not ((lectureId is not None) and (eoa is not None)):
            return Response({"user": None, "message": "アカウントアドレスが指定されていません"}, status=status.HTTP_400_BAD_REQUEST)
        # ユーザーのレクチャーを全て取得
        # レクチャーにいいねしたユーザーで同期がfalseのものの個数を計算
        user = CustomeUser.objects.filter(eoa=eoa).get()
        lecture = Lecture.objects.get(id=lectureId)
        try:
            Favorite.objects.create(user=user, lecture=lecture)
            if lecture.favo is None:
                lecture.favo = 0
            lecture.favo += 1
            lecture.save()
            return Response({"message": "勉強会にいいねしました"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "勉強会が見つかりませんでした"}, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    @action(detail=False, methods=[HttpMethod.PUT.name])
    def update_to_sync(self, request: Request, *args, **kwargs):
        id = request.data.get("id")
        try:
            favo = Favorite.objects.get(id=id)
            favo.is_synced = True
            favo.save()
            return Response({"message": "オンチェーンにいいねを同期しました"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "オンチェーンへのいいねを同期に失敗しました"}, status=status.HTTP_404_NOT_FOUND)

    # @transaction.atomic
    # def destroy(self, request: Request, *args, **kwargs):
    #     favoriteId = request.data.get("id")
    #     favorite = Favorite.objects.get(id=favoriteId)
    #     if favorite is None:
    #         return Response({"user": None, "message": "いいねが存在しません"}, status=status.HTTP_400_BAD_REQUEST)
    #     try:
    #         lecture = favorite.lecture
    #         lecture.favo -= 1
    #         lecture.save()
    #         favorite.delete()
    #         return Response({"message": "勉強会を取り消しました。"}, status=status.HTTP_200_OK)
    #     except:
    #         return Response({"message": "いいねが見つかりませんでした"}, status=status.HTTP_404_NOT_FOUND)
