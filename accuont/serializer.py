from rest_framework import serializers
from .models import Depatment

class DepartmentSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Depatment
        fields = "__all__"