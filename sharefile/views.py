# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.views import APIView
from django.http import request
from rest_framework.response import Response
from collections import OrderedDict

from sharefile.serializers import  *
from sharefile.models import *

from api.models import *
from api.views import *
from api.serializers import *
import random



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
        msg = request.query_params.dict()["filename"]
        response = BaseResponse()
        response.data = "null"
        response.code = "200"
        response.msg = "ok"
        return JsonResponse(response.dict)
    def post(self,request):
        msg = request.data.get('filename')
        print(msg)
        response = BaseResponse()
        response.data = "null"
        response.code = "200"
        response.msg = "ok"
        return JsonResponse(response.dict)


class ShareToFile(APIView):
    def post(self, request):
        response = BaseResponse()
        try:
            fileids = request.data.get('fileids')
            type = request.data.get('type')

            # 产生4位随机数
            random_str = str(random.randint(1000, 9999))

            if type == "img":
                for fileid in fileids:
                    print(str(fileid) + type + random_str)
                    file = Img.objects.get(fileid=fileid)
                    share = Share.eobjects.create(file_id=fileid, type=type, path=file.path, share_no=random_str)
            elif type == "doc":
                for fileid in fileids:
                    print(str(fileid) + type + random_str)
                    file = Doc.objects.get(fileid=fileid)
                    share = Share.objects.create(file_id=fileid, type=type, path=file.path, share_no=random_str)
            elif type == "radio":
                for fileid in fileids:
                    print(str(fileid) + type + random_str)
                    file = Radio.objects.get(fileid=fileid)
                    share = Share.objects.create(file_id=fileid, type=type, path=file.path, share_no=random_str)
            elif type == "video":
                for fileid in fileids:
                    print(str(fileid) + type + random_str)
                    file = Video.objects.get(fileid=fileid)
                    share = Share.objects.create(file_id=fileid, type=type, path=file.path, share_no=random_str)

            response.code = "200"
            response.msg = "ok"
            response.data = random_str
            return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            response.data = "null"
            return JsonResponse(response.dict)


class ShareShowFile(APIView):
    def get(self, request):
        response = BaseResponse()
        try:
            share_no = request.query_params.dict()["shareno"]
            data = []
            share_list = Share.objects.filter(share_no = share_no)
            share_list = ShareSerializer(share_list, many=True)
            data.append(share_list.data)
            response.data = data
            response.code = "200"
            response.msg = "ok"
            return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            response.data = "null"
            return JsonResponse(response.dict)


class ShareSaveFile(APIView):
    def post(self, request):
        response = BaseResponse()
        try:
            type = request.data.get('type')
            # 列表
            fileids = request.data.get('fileids')
            userid = request.data.get('userid')
            shareno = request.data.get('shareno')

            if type == "img":
                for fileid in fileids:
                    print(str(fileid) + type + shareno + str(userid))
                    file = Img.objects.get(fileid=fileid)
                    img = Img.objects.create(filename=file.filename, type=type, size=file.size, path=file.path,
                                             user_id=userid)
                Share.objects.filter(share_no = shareno).delete()
            elif type == "doc":
                for fileid in fileids:
                    print(str(fileid) + type + shareno + str(userid))
                    file = Doc.objects.get(fileid=fileid)
                    img = Doc.objects.create(filename=file.filename, type=type, size=file.size, path=file.path,
                                             user_id=userid)
                Share.objects.filter(share_no=shareno).delete()
            elif type == "radio":
                for fileid in fileids:
                    print(str(fileid) + type + shareno + str(userid))
                    file = Radio.objects.get(fileid=fileid)
                    img = Radio.objects.create(filename=file.filename, type=type, size=file.size, path=file.path,
                                               user_id=userid)
                Share.objects.filter(share_no=shareno).delete()
            elif type == "video":
                for fileid in fileids:
                    print(str(fileid) + type + shareno + str(userid))
                    file = Video.objects.get(fileid=fileid)
                    img = Video.objects.create(filename=file.filename, type=type, size=file.size, path=file.path,
                                               user_id=userid)
                Share.objects.filter(share_no=shareno).delete()
            response.data = "null"
            response.code = "200"
            response.msg = "ok"
            return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            response.data = "null"
            return JsonResponse(response.dict)
