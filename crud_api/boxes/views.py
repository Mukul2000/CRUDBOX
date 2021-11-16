from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Box
from .serializers import BoxSerializer

# Create your views here.
class BoxView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):

        user = request.user

        if user.is_staff == False:
            return Response({"error": ["You don't have sufficient permissions"]},
                        status=status.HTTP_403_FORBIDDEN)

        l = request.data.get('length', None)
        b = request.data.get('breadth', None)
        h = request.data.get('height', None)

        if l == None or b == None or h == None:
            return Response({"error": ["Invalid dimensions"]}, 
                status=status.HTTP_400_BAD_REQUEST)

        l = float(l)
        b = float(b)
        h = float(b)

        box = Box.objects.create(length=l, breadth=b, height=h, created_by = user)
        
        return Response(BoxSerializer(box).data,status=status.HTTP_200_OK)