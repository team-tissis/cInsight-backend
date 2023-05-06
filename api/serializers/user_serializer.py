from rest_framework import serializers 
from api.models import CustomUser
 
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
