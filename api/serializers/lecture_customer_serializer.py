from rest_framework import serializers 
from api.serializers.user_serializer import UserSerializer
from api.serializers.lecture_serializer import PureLectureSerializer

class LectureCustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(required=False)
    lecture = PureLectureSerializer(many=False, read_only=True)
    lecture_id = serializers.IntegerField(required=False)
