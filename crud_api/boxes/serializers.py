from rest_framework import serializers

class BoxSerializer(serializers.Serializer):
    length = serializers.FloatField()
    breadth = serializers.FloatField()
    height = serializers.FloatField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
