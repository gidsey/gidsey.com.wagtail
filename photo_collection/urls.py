from django.urls import path

from .views import PhotoDetailPage

app_name = 'photo_collection'

urlpatterns = [
    path('collections/photo/<id>', PhotoDetailPage.as_view(), name='photo-detail'),
]