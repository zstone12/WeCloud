from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
# Create your views here.
from rest_framework.views import APIView
from django.http import request
from rest_framework.response import Response
from api.serializers import  *
from api.models import  *


class BaseResponse(object):
    def __init__(self):
        self.code = 200
        self.msg = ""
        self.data = None

    @property
    def dict(self):
        return self.__dict__


class Test(APIView):
    def get(self,request):
        response=BaseResponse()
        data=User.objects.all()
        data=UserSerializer(data,many=True)
        response.data=data.data
        response.code=200
        response.msg="查询成功"
        return JsonResponse(response.dict)


class CheckUsername(APIView):
    def get(self,request):
        response = BaseResponse()

        username = request.query_params.dict()["username"]
        try:
            user = User.objects.get(username=username)
            response.code = "200"
            response.msg = "yes"
            response.data="null"
        except:
            response.code="201"
            response.msg="no"
            response.data = "null"
        finally:
            return JsonResponse(response.dict)


class CheckEmail(APIView):
    def get(self,request):
        response = BaseResponse()
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            response.code = "200"
            response.msg = "yes"
            response.data = "null"
        except:
            response.code = "201"
            response.msg = "no"
            response.data = "null"
        finally:
            return JsonResponse(response.dict)
