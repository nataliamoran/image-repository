from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.DefaultRouter()
router.register(r'images', views.ImageView, basename='image')
# router.register('images', views.ImageView.as_view({'get': 'list'}), 'image')
# router.register(r'images', views.list_image)
# router.register(r'images/<int:pk>/', views.manage_image)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# urlpatterns = [
#     path('images/', views.ImageView.as_view()),
#     path('images/<int:pk>/', views.ImageView.as_view()),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)