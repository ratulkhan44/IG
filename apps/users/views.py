# Django Imports
from django.shortcuts import render
from rest_framework import status, permissions,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# self Imports
from .models import User
from .serializers import UserSerializer,UserLoginSerializer
from rest_framework.exceptions import ValidationError, AuthenticationFailed

# Create your views here.
class UserRegistrationView(APIView):
    '''
        This code block contains code which are related to register a user.
    '''
    
    def post(self,request,*args,**kwargs):
        try:
            if request.method == 'POST':
                print("********  Request Data *********",request.data)
                if not request.data.get("email",None):
                    return Response({"success": False, "message": "Email cannot be empty", "data": []}, status=status.HTTP_400_BAD_REQUEST)
                if not request.data.get("mobile",None):
                    return Response({"success": False, "message": "Mobile cannot be empty", "data": []}, status=status.HTTP_400_BAD_REQUEST)
                if not request.data.get("password",None):
                    return Response({"success": False, "message": "Password cannot be empty", "data": []}, status=status.HTTP_400_BAD_REQUEST)
                if User.objects.filter(email = request.data.get("email",None)).exists():
                    return Response({"success": False, "message": "A user with that email already exists!", "data": []}, status=status.HTTP_400_BAD_REQUEST)
                
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    user_serializer.save()
                    return Response({"success": True, "message": "User created successfully!", "data": []}, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            print(e.args[0])
            return Response({"success": False, "message": str(e), "data": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Investor & Trader login
class UserLoginView(generics.GenericAPIView):

    serializer_class = UserLoginSerializer
    
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(
                {
                    "success": True,
                    "message": "Successfully Login",
                    "data": serializer.data
                }
            )
        except ValidationError as e:
            error_detail = e.detail
            formatted_errors = {key: [str(value[0])] for key, value in error_detail.items()}
            return Response(
                {
                    "success": False,
                    "message": "",
                    "error": formatted_errors
                }
            )
        except AuthenticationFailed as e:
            return Response(
                {
                    "success": False,
                    "message": e.detail,
                    "error": {}
                }
            )
            
            
class UserLogoutView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token is required.'}, status=400)
        try:
            refresh_token_obj = RefreshToken(refresh_token)
            refresh_token_obj.blacklist()
            return Response(
                {
                    'success': True,
                    'message': 'Successfully logged out.',
                    'data': {}
                }
            )
        except Exception as e:
            print(e.args[0])
            return Response(
                {
                    'success': False,
                    'error': 'Invalid refresh token.',
                    'data': {}
                }
            )


