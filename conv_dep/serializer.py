
from rest_framework import serializers

from conv_dep.models import Utterance, Conv


class ConvDepSerializer(serializers.ModelSerializer):
    conv_id = serializers.IntegerField(source='conv.id', read_only=True)

    class Meta:
        model = Utterance
        fields = ('conv_id', 'utr_id', 'word_id', 'word')


class ConvDepIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conv
        fields = '__all__'