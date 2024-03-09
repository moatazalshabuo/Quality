from rest_framework import serializers
from .models import *

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'