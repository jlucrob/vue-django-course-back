from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from users.serializers import UserSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.http import HttpResponse


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    @method_decorator(csrf_protect)
    def post(self, request):
        username = request.data.get('username', '').strip().lower()
        password = request.data.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                serializer = UserSerializer(user)    
                return Response(serializer.data, content_type="application/json")
            else:
                return Response({'error': 'Your account is deactivated.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Username and password don\'t match.'}, status=status.HTTP_400_BAD_REQUEST)


class CSRFTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
       return HttpResponse()


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return Response()


class UserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'user': serializer.data}, status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)