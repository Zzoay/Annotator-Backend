
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from common.models import User, Process, ProcessAssignment
from common.serializer import UserSerializer, UserLoginSerializer, ProcessSerializer, ProcessAssignSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginViewSet(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()


    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
        else:
            ret = {'detail': '用户名或密码错误'}
            return Response(ret, status=403)


class UserLogoutViewSet(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserLoginSerializer

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({'detail': 'logout successful !'})


class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all().order_by('created_at')
    serializer_class = ProcessSerializer

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId', None)
        queryset = self.queryset.filter(user=user_id) 
        serializer = self.serializer_class(queryset, many=True)

        data = serializer.data
        return Response(data)


class ProcessAssignViewSet(viewsets.ModelViewSet):
    queryset = ProcessAssignment.objects.all().order_by('created_at')
    serializer_class = ProcessAssignSerializer

    def list(self, request, *args, **kwargs):
        process_id = request.query_params.get('processId', None)
        queryset = self.queryset.filter(process=process_id) 
        serializer = self.serializer_class(queryset, many=True)

        data = serializer.data
        return Response(data)
