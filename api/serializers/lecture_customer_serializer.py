from rest_framework import serializers 
from api.models import Lecture, CustomeUser, Favorite
from api.serializers.user_serializer import UserSerializer
from api.serializers.lecture_serializer import PureLectureSerializer

class LectureCustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(required=False)
    lecture = PureLectureSerializer(many=False, read_only=True)
    lecture_id = serializers.IntegerField(required=False)

    class Meta:
        model = Favorite
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
