
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from conv_dep import views


router = DefaultRouter()
router.register('conv', views.ConvViewSet)
router.register('conv_dep', views.ConvDepViewSet)
router.register('relation', views.RelationViewSet)
router.register('relationship', views.RelationshipViewSet)
router.register('word', views.WordViewSet)


urlpatterns = [
    path('', include(router.urls)),
]