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

        user = request.user
        if user.is_staff == False:
            return Response({"error": ["You don't have sufficient permissions"]},
                        status=status.HTTP_403_FORBIDDEN)

        box_id = self.kwargs.get('id',None)

        if box_id is None:
            # fetch all of this user's boxes
            boxes = Box.objects.filter(created_by = user)

            return Response(BoxSerializer(boxes, many = True).data, status = status.HTTP_200_OK) 
        else:
          # fetch a particular box
            try:
                box = Box.objects.get(id=box_id)
            except Box.DoesNotExist:
                return Response({'error': ['No box with this id']},
                        status = status.HTTP_404_NOT_FOUND)         
            
            return Response(BoxSerializer(box).data, status=status.HTTP_200_OK)


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

    def put(self, request, *args, **kwargs):

        user = request.user

        if user.is_staff == False:
            return Response({"error": ["You don't have sufficient permissions"]},
                        status=status.HTTP_403_FORBIDDEN)

        box_id = self.kwargs.get('id', None)

        if box_id is None:
            return Response({'id': ['This field is required']},
                        status=status.HTTP_400_BAD_REQUEST)

        try:
            box = Box.objects.get(id=box_id)
        except Box.DoesNotExist:
            return Response({'error': ['No box with this id']},
                        status = status.HTTP_404_NOT_FOUND)

        l = request.data.get('length', None)
        h = request.data.get('breadth', None)
        b = request.data.get('height', None)

        if l is not None:
            box.length = float(l)
        if b is not None:
            box.breadth = float(b) 
        if h is not None:
            box.height = float(h)

        box.save()

        return Response(BoxSerializer(box).data, status = status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):

        user = request.user

        box_id = self.kwargs.get('id', None)

        if box_id is None:
            return Response({'id': ['This field is required']},
                        status=status.HTTP_400_BAD_REQUEST)

        try:
            box = Box.objects.get(id=box_id)
        except Box.DoesNotExist:
            return Response({'error': ['No box with this id']},
                        status = status.HTTP_404_NOT_FOUND)

        if user != box.created_by:
            return Response({'error': ['You are not the creator of this box']},
                            status = status.HTTP_403_FORBIDDEN)

        box.delete()

        return Response({'message': ['Box successfully deleted']}, status=status.HTTP_200_OK)