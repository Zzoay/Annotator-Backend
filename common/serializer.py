
from rest_framework import serializers
from common.models import User, Process, ProcessAssignment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'created_at', 'nickname']


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ['id', 'task', 'user', 'assign_num', 'finished_num']


class ProcessAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessAssignment
        fields = ['id', 'process', 'item_id', 'status']