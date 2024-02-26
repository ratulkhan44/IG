from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer


class ImageAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        try:
            queryset = Image.objects.all().order_by('-id')
            serializers =  ImageSerializer(queryset, many=True)
            if queryset:
                return Response(
                    {
                        "success": True,
                        "message": "Image list",
                        "data": serializers.data
                    },
                    status=status.HTTP_200_OK
                )
            
            else:
                return Response(
                    {
                        "success": True,
                        "message": "No Image found!",
                        "data": ""
                    },
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response({"success": False, "message": str(e), "data": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request,*args,**kwargs):
        try:
            image_data = request.data
            image_data['created_by'] = request.user.id
            image_data['view_count'] = 0
            image_serializer = ImageSerializer(data=image_data)
            if image_serializer.is_valid():
                image_serializer.save()
                return Response({"success": True, "message": "Image created successfully!", "data": image_serializer.data}, status=status.HTTP_201_CREATED)
            print(image_serializer.errors)
            return Response({"success": False, "message": "Image successfully not created", "data": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            print(e.args[0])
            return Response({"success": False, "message": str(e), "data": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self,request,img_id,*args,**kwargs):
        try:
            image = Image.objects.get(id = img_id)
            image_data = request.data
            image_data['created_by'] = request.user.id
            image_data['view_count'] = 1000
            image_serializer = ImageSerializer(instance=image,data = image_data)
            if image_serializer.is_valid():
                image_serializer.save()
                return Response({"success": True, "message": "Image Update successfully!", "data": image_serializer.data}, status=status.HTTP_201_CREATED)
            print(image_serializer.errors)
            return Response({"success": False, "message": "Image successfully not Update", "data": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            print(e.args[0])
            return Response({"success": False, "message": str(e), "data": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def delete(self,request,img_id,*args,**kwargs):
        try:
            image = get_object_or_404(Image, id=img_id)
            image.delete()
            return Response({"success": True, "message": "Image Delete successfully!", "data": []}, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(e.args[0])
            return Response({"success": False, "message": str(e), "data": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

