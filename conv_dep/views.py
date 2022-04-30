import re
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from conv_dep.models import Utterance, Conv
from conv_dep.serializer import ConvDepSerializer, ConvDepIdSerializer


class ConvDepViewSet(viewsets.ModelViewSet):
    queryset = Utterance.objects.all()
    serializer_class = ConvDepSerializer

    def list(self, request, *args, **kwargs):
        conv_id = request.query_params.get('convId', None)
        self.queryset = self.queryset.filter(conv=conv_id) 
        serializer = self.serializer_class(self.queryset, many=True)

        data = serializer.data
        utr_id_set, utr_lst = {}, []
        for d in data:
            utr_id = d['utr_id']
            if utr_id not in utr_id_set.keys():
                utr_id_set[utr_id] = len(utr_id_set)  # save index
                utr_lst.append({
                    'id': utr_id,
                    'items': [{'id': d['word_id'], 'word': d['word']}]
                })
            else:
                utr_lst[utr_id_set[utr_id]]['items'].append({
                    'id': d['word_id'], 
                    'word': d['word']
                })
        return Response(utr_lst)


class ConvDepIdsViewSet(viewsets.ModelViewSet):
    queryset = Conv.objects.all()
    serializer_class = ConvDepIdSerializer

    # def list(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(self.queryset, many=True)
    #     res_lst = []
    #     for d in serializer.data:
    #         res_lst.append({
    #         })
    #     return Response(res_lst)
