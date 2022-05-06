
from rest_framework import serializers

from conv_dep.models import Utterance, Conv, Relation, Relationship


class ConvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conv
        fields = '__all__'


class ConvDepSerializer(serializers.ModelSerializer):
    conv_id = serializers.IntegerField(source='conv.id', read_only=True)

    class Meta:
        model = Utterance
        fields = ('conv_id', 'utr_id', 'word_id', 'word')


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = '__all__'


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = '__all__'