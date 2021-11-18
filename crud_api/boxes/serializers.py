from rest_framework import serializers
from users.models import User
from .models import Box

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__' 
        model = Box

class StoreBoxSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['length', 'breadth', 'height']
        model = Box
