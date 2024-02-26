# Django Imports
from django.urls import path
from .views import ImageAPIView

urlpatterns = [
    path('image-create/', ImageAPIView.as_view()),
    path('image-list/', ImageAPIView.as_view()),
    path('image-update/<int:img_id>', ImageAPIView.as_view()),
    path('image-delete/<int:img_id>', ImageAPIView.as_view()),
]