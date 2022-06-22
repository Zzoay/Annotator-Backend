
from rest_framework import serializers

from conv_dep.models import Utterance, Conv, Relation, Relationship, Word


class ConvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conv
        fields = '__all__'


class ConvDepSerializer(serializers.ModelSerializer):
    # conv_id = serializers.IntegerField(source='conv.id')

    class Meta:
        model = Utterance
        fields = '__all__'


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = '__all__'


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields ='__all__'