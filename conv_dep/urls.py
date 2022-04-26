
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from conv_dep import views


router = DefaultRouter()
router.register('conv_dep', views.ConvDepViewSet)
router.register('conv_dep_ids', views.ConvDepIdsViewSet)


urlpatterns = [
    path('', include(router.urls)),
]