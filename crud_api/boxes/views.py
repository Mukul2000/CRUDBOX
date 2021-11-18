from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Box, BoxLimits
from .serializers import BoxSerializer, StoreBoxSerializer

# Create your views here.
class BoxView(APIView):

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        user = request.user
        box_id = self.kwargs.get('id',None)

        if box_id is None:
            # fetch all of this user's boxes
            boxes = BoxUtils.filter_boxes(user, request.query_params)

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


class BoxStoreView(APIView):
    permissions=[permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        user = request.user
        boxes = BoxUtils.filter_boxes(user, request.query_params)

        return Response(StoreBoxSerializer(boxes, many = True).data, status=status.HTTP_200_OK)

class BoxUtils:


    def filter_boxes(user, filters):
        query_filters = ['l_lte', 'l_gte', 'b_lte', 'b_gte', 'h_lte', 'h_gte', 'a_lte', 'a_gte', 'v_lte', 'v_gte', 'created_by']

        boxes = Box.objects.all()
        for f in query_filters:
            if f in filters:
                value = float(filters[f])
                if f[0] == 'l':
                   if f == 'l_lte': 
                       boxes = boxes.filter(length__lte = value)
                   if f == 'l_gte':
                       boxes = boxes.filter(length__gte = value)

                elif f[0] == 'b':
                    if f == 'b_lte': 
                       boxes = boxes.filter(breadth__lte = value)
                    if f == 'b_gte':
                       boxes = boxes.filter(breadth__gte = value)

                elif f[0] == 'h':
                    if f == 'h_lte': 
                        boxes = boxes.filter(height__lte = value)
                    if f == 'h_gte':
                        boxes = boxes.filter(height__gte = value)

                elif f[0] == 'a':
                    if f == 'a_lte': 
                        boxes = [BoxUtils.get_area(box) <= value for box in boxes]
                    if f == 'a_gte':
                        boxes = [BoxUtils.get_area(box) >= value for box in boxes]

                elif f[0] == 'v':
                    if f == 'v_lte':
                        boxes = [BoxUtils.get_volume(box) <= value for box in boxes]
                    if f == 'v_gte':
                        boxes = [BoxUtils.get_volume(box) >= box.length * box.breadth * box.height >= value for box in boxes]

                elif f == 'created_by':
                    boxes = boxes.filter(created_by__id=int(value))
        return boxes

    @staticmethod
    def get_volume(box):
        return box.length*box.breadth*box.height

    @staticmethod
    def get_area(box):
        return 2*(box.length * box.breadth + box.length*box.height + box.breadth*box.height)