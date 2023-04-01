from django.db.models import QuerySet
from django_filters import rest_framework as filters
from rest_framework import viewsets, status

from api.filters import CustomPagination, NoPagination
from api.models import Lecture, CustomeUser, LectureCustomer
from api.serializers.lecture_customer_serializer import LectureCustomerSerializer

from rest_framework.decorators import action
from api.utils import HttpMethod
from django.db import transaction
from rest_framework.request import Request
from rest_framework.response import Response

class LectureCustomerFilter(filters.FilterSet):
    class Meta:
        model = LectureCustomer
        fields = "__all__"


class LectureCustomerViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[LectureCustomer] = LectureCustomer.objects.all()
    serializer_class = LectureCustomerSerializer
    filter_class = LectureCustomerFilter
    pagination_class = CustomPagination

    @transaction.atomic
    @action(detail=False, methods=[HttpMethod.POST.name])
    def simple_create(self, request: Request, *args, **kwargs):
        lectureId = request.data.get("lecture_id")
        eoa = request.data.get("eoa")

        if not ((lectureId is not None) and (eoa is not None)):
            return Response({"message": "アカウントアドレスが指定されていません"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomeUser.objects.filter(eoa=eoa).get()
        lecture = Lecture.objects.get(id=lectureId)

        if (LectureCustomer.objects.filter(user=user, lecture=lecture) is not None):
            return Response({"message": "すでに参加登録しています"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            LectureCustomer.objects.create(user=user, lecture=lecture)
            return Response({"message": "勉強会に参加登録しました"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "勉強会に参加登録できませんでした"}, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    @action(detail=False, methods=[HttpMethod.GET.name])
    def index(self, request: Request, *args, **kwargs):
        lectureId = request.query_params.get("lecture_id")

        if not (lectureId is not None):
            return Response({"user": None, "message": "勉強会IDが指定されていません"}, status=status.HTTP_400_BAD_REQUEST)

        lecture = Lecture.objects.get(id=lectureId)
        joined_customers =  LectureCustomer.objects.filter(lecture=lecture)
        customers = [ {
                        "id": lecture_customer.user.id,
                        "eoa": lecture_customer.user.eoa
            } for lecture_customer in joined_customers
        ]

        try:
            return Response({"result": customers}, status=status.HTTP_200_OK)
        except:
            return Response({"result": []}, status=status.HTTP_404_NOT_FOUND)
