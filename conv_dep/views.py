from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from conv_dep.models import Utterances, UtrsIds
from conv_dep.serializer import ConvDepSerializer, ConvDepIdSerializer


class ConvDepViewSet(viewsets.ModelViewSet):
    queryset = Utterances.objects.all()
    serializer_class = ConvDepSerializer


class ConvDepIdsViewSet(viewsets.ModelViewSet):
    queryset = UtrsIds.objects.all()
    serializer_class = ConvDepIdSerializer


# @api_view(['GET'])
# def getUtterances(request, UtrsId):
#     try:
#         snippet = Utterances.objects.get(id=UtrsId)
#     except Utterances.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = ConvDepSerializer(snippet)
#         return Response(serializer.data)


# def conv_dep(request):
#     utterance_id = request.POST['id']
#     utterance = Utterances.objects.get(id=utterance_id)
#     return HttpResponse(utterance)