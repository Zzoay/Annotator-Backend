import re
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from regex import W
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from conv_dep.models import Utterance, Conv, Relation, Relationship, Word
from conv_dep.serializer import ConvSerializer, ConvDepSerializer, RelationSerializer, RelationshipSerializer, WordSerializer


class ConvViewSet(viewsets.ModelViewSet):
    queryset = Conv.objects.all()
    serializer_class = ConvSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.queryset.filter(status=0)  # 检索未标注的数据
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data[0])  # 返回第一个
        except IndexError:  # 如果全都已标注，则返回最后一个
            serializer = self.serializer_class(self.queryset, many=True)
            return Response(serializer.data[-1]) 
    
    # 通过many=True直接改造原有的API，使其可以批量创建
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if isinstance(self.request.data, list):
            return serializer_class(many=True, *args, **kwargs)
        else:
            return serializer_class(*args, **kwargs)


class ConvDepViewSet(viewsets.ModelViewSet):
    queryset = Utterance.objects.all()
    serializer_class = ConvDepSerializer

    def list(self, request, *args, **kwargs):
        conv_id = request.query_params.get('convId', None)
        queryset = self.queryset.filter(conv=conv_id) 
        serializer = self.serializer_class(queryset, many=True)

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
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if isinstance(self.request.data, list):
            return serializer_class(many=True, *args, **kwargs)
        else:
            return serializer_class(*args, **kwargs)


class RelationViewSet(viewsets.ModelViewSet):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer


class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer

    def list(self, request, *args, **kwargs):
        conv_id = request.query_params.get('convId', None)
        queryset = self.queryset.filter(conv=conv_id) 
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)
    
    def update(self, instance, validated_data):
        instance.relation = validated_data['relation']
        instance.save()
        return instance


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if isinstance(self.request.data, list):
            return serializer_class(many=True, *args, **kwargs)
        else:
            return serializer_class(*args, **kwargs)