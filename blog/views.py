from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from blog.models import Article,User,Profile
from blog.serializers import ArticleSerializer,UserSerializer,ProfileSerializer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics
from rest_framework import permissions
from blog.permissions import IsOwnerOrReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from blog.pagination import MyPageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from blog.filters import ArticleFilter
from blog.throttles import ArticleListAnonRateThrottle,ArticleListUserRateThrottle

from rest_framework.renderers import coreapi

# Create your views here.


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    # authentication_classes = [TokenAuthentication,]

    pagination_class = MyPageNumberPagination

    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class=ArticleFilter
    ordering_fields=['create_date',]

    # throttle_classes = [ArticleListAnonRateThrottle,ArticleListUserRateThrottle,]
    # throttle_scope='article_list'




class ArticleDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    def get_object(self,pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404
    def get(self,request,pk,format=None):
        article=self.get_object(pk)
        serializer=ArticleSerializer(article)
        return Response(serializer.data)
    def put(self,request,pk,format=None):
        article=self.get_object(pk)
        serializer=ArticleSerializer(instance=article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        article=self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(APIView):
    def get(self,request,format=None):
        users=User.objects.all()
        serializer=UserSerializer(users,many=True)
        return Response(serializer.data)
    def post(self,request,format=None):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class ProfileList(APIView):
    # 'addr', 'user'
    coreapi_fields =[
        coreapi.Field(name='addr',location='query',description='地址'),
        # coreapi.Field(name='user',location='query',description='用户id')
    ]
    def get(self,request,format=None):
        profiles=Profile.objects.all()
        serializer=ProfileSerializer(profiles,many=True)
        return Response(serializer.data)
    # @AutoSchema
    def post(self,request,format=None):
        serializer=ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print('测试data',serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(
            data=request.data,
            context={'request':request}
        )
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token,created=Token.objects.get_or_create(user=user)
        return Response(
            {
                'token':token.key,
                'user_id':user.id,
                'email':user.email
            }
        )