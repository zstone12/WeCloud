from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
# Create your views here.
from rest_framework.views import APIView
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