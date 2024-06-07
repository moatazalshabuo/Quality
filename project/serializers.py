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
        
class Quality_standardsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Quality_standards
        fields = '__all__'
        
class StandardAccSerializer(serializers.ModelSerializer):
    quality_standards = Quality_standardsSerializers()
    class Meta:
        model = StandardAcc
        fields = '__all__'