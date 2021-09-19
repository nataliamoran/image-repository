from django.http import JsonResponse
from rest_framework.decorators import action

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

    @action(detail=False, methods=['delete'])
    def delete_multiple(self, request):
        to_be_deleted_list = request.query_params.get('ids', '').split(',')
        deleted_list = []
        not_deleted_list = []
        for image_id in to_be_deleted_list:
            try:
                image_id = int(image_id)
            except ValueError:
                not_deleted_list.append(image_id)
                continue
            deleted, _ = self.get_queryset().filter(id=image_id, owner=request.user).delete()
            target_list = deleted_list if deleted else not_deleted_list
            target_list.append(image_id)
        return JsonResponse({'deleted': deleted_list,
                             'not_deleted': not_deleted_list},
                            status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], )
    def create_multiple(self, request):
        create_list = request.data
        created_list = []
        failed_list = []
        for item in create_list:
            serializer = ImageCreateSerializer(data=item, context={'request': request, })
            if not serializer.is_valid():
                failed_list.append(item)
                continue
            self.perform_create(serializer)
            created_list.append(serializer.data)
        return JsonResponse({'created': created_list,
                             'failed': failed_list},
                            status=status.HTTP_201_CREATED)