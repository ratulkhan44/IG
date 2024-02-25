# Django Imports
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

# Self Imports
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(required=True)
    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
    
    class Meta:
        model = User
        fields = ['email', 'mobile','is_verified', 'is_active','password', 'created_at', 'updated_at']


class UserLoginSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(max_length=255) 
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )
    username = serializers.CharField(read_only=True)
    mobile = serializers.CharField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    
    
    def get_token(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }