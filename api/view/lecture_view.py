from django.db.models import QuerySet
from django_filters import rest_framework as filters
from rest_framework import viewsets, status

from api.filters import CustomPagination, NoPagination
from api.models import Lecture
from api.serializers.lecture_serializer import PureLectureSerializer, DetailLectureSerializer

from rest_framework.decorators import action
from api.utils import HttpMethod
from django.db import transaction

from rest_framework.request import Request
from rest_framework.response import Response

class LectureFilter(filters.FilterSet):
    class Meta:
        model = Lecture
        fields = "__all__"
        exclude = ["attendee_eoas"]


class LectureViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Lecture] = Lecture.objects.all()
    serializer_class = PureLectureSerializer
    filter_class = LectureFilter
    pagination_class = CustomPagination
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DetailLectureSerializer(instance)
        return Response({"lecture": serializer.data}, status=status.HTTP_200_OK)

    
    @transaction.atomic
    @action(detail=False, methods=[HttpMethod.PUT.name])
    # 勉強会に対するいいねの数を更新
    def favo(self, request: Request, *args, **kwargs):
        lectureId = request.data.get("lecture_id")
        # eoa = request.data.get("eoa") # いいねを押したユーザーの情報は、スマコンで保持
        favoNum = request.data.get("favo_newly_added")
        
        if lectureId is None:
            return Response({"user": None, "message": "勉強会IDが指定されていません"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                lecture = Lecture.objects.get(id=lectureId)
                if lecture.favo is None:
                    lecture.favo = 0
                lecture.favo += favoNum
                lecture.save()
                return Response({"message": "勉強会にいいねしました"}, status=status.HTTP_200_OK)
            except:
                return Response({"message": "勉強会が見つかりませんでした"}, status=status.HTTP_404_NOT_FOUND)
    