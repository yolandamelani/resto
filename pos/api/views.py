from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .paginators import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
# from pos_app.models import (
#     User, StatusModel, Profile, TableResto, Category, MenuResto, OrderMenu, OrderMenuDetail,
# )  
from app_pos.models import (
    User, TableResto, StatusModel, MenuResto
)
from api.serializers import (
    LoginSerializer, RegisterUserSelializer, TableRestoSerializer, MenuRestoSerializer,
)

# from api.serializers import (
#     LoginSerializer, UserSerializer, ProfileSerializer, ProfileSerializerII, RegisterUserSelializer,
#      StatusModelSerializer, TableRestoSerializer, CategorySerializer, MenuRestoSerializer,
# )

from rest_framework import generics

class TableRestoListApiView(APIView):

    def get(self, request, *args, **kwargs):
        table_restos = TableResto.objects.all()
        serializer = TableRestoSerializer(table_restos, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, *args,**kwargs):
        data = {
            'code' : request.data.get('code'),
            'name' : request.data.get('name'),
            'capacity' : request.data.get('capacity'),
        }
        serializer = TableRestoSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Data created successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class TableRestoDetailApiView(APIView):

    def get_object(self, id):
        try:
            return TableResto.objects.get(id = id)
        except TableResto.DoesNotExist:
            return None
        
    def get(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
        if not table_resto_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists...',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TableRestoSerializer(table_resto_instance)
        response = {
            'status' : status.HTTP_400_BAD_REQUEST,
            'message' : 'Data retrieve successfully...',
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
        if not table_resto_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists...',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'code' : request.data.get('code'),
            'name' : request.data.get('name'),
            'capacity' : request.data.get('capacity'),
            'table_status' : request.data.get('table_status'),
            'status' : request.data.get('status'),
        }
        serializer = TableRestoSerializer(instance = table_resto_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : 'Data updated successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
        if not table_resto_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data does not exists...',
                    'data' : {}
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        table_resto_instance.delete()
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Data deleted successfully...'
        }
        return Response(response, status = status.HTTP_200_OK)
    
class RegisterUserAPIView(APIView):
    serializer_class = RegisterUserSelializer

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Selamat anda telah terdaftar...',
                'data' : serializer.data,
            }
            return Response(response_data, status = status.HTTP_201_CREATED)
        return Response({
            'status' : status.HTTP_400_BAD_REQUEST,
            'data' : serializer.errors
        },status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token, created = Token.objects.get_or_create(user = user)
        return JsonResponse({
            'status' : 200,
            'message' : 'Selamat anda berhasil masuk...',
            'data' : {
                'token' : token.key,
                'id' : user.id,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'email' : user.email,
                'is_active' : user.is_active,
                'is_waitress' : user.is_waitress,
            }
        })
    
class MenuRestoView(APIView):
    authentication_class = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwrgs):
        menu_restos = MenuResto.objects.select_related('status').\
            filter(status = StatusModel.objects.first())
        serializer = MenuRestoSerializer(menu_restos, many = True, )
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Pembacaan seluruh data berhasil...',
            'user' : str(request.user),
            'auth' : str(request.auth),
            'data' : serializer.data,
        }
        return Response(response, status = status.HTTP_200_OK)

class MenuRestoFilterAPi(generics.ListAPIView):
    queryset = MenuResto.objects.all()
    serializer_class = MenuRestoSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category__name']
    ordering_fields = ['created_on']