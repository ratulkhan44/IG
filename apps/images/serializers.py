# Django Imports
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.users.serializers import UserSerializer
# Self Imports
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    # created_by = UserSerializer(many=False)

    class Meta:
        model = Image
        fields = ['name', 'image_file','view_count', 'created_by','created_at', 'updated_at']

