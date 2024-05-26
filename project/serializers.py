from rest_framework import serializers
from .models import *

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'
        
        
class AccStatusMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccStatusMain
        fields = '__all__'