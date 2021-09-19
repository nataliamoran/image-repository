from django.http import JsonResponse

from .models import Image
from rest_framework import viewsets, permissions, status
from .serializers import ImageSerializer, ImageCreateSerializer
from rest_framework.response import Response


class ImageView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ImageCreateSerializer
        return ImageSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'detail': 'Only image owner can delete the image.'}, status=status.HTTP_403_FORBIDDEN)



