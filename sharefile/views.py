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
        self.code = "201"
        self.msg = "null"
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
        data = request.data
        # msg = request.data.get('filename')
        msg = data['data']['filename']
        print(msg)
        response = BaseResponse()
        response.data = "null"
        response.code = "200"
        response.msg = "ok"
        return JsonResponse(response.dict)


class ShareToFile(APIView):
    def post(self, request):
        response = BaseResponse()
        #try:
            # fileids = request.data.get('fileids')
            # type = request.data.get('type')
        data = request.data
        # print(data)
        fileids = data['data']['fileids']
        type = data['data']['type']
        userid =request.session['userid']
        

        # 产生4位随机数
        random_str = str(random.randint(1000, 9999))

        if type == "img":
            for fileid in fileids:
                print(str(fileid) + type + random_str)
                file = Img.objects.get(file_id=fileid)
                share = Share.objects.create(file_id=fileid, type=type, path=file.path, share_no=random_str)
        elif type == "doc":
            for fileid in fileids:
                print(str(fileid) + type + random_str)
                file = Doc.objects.get(file_id=fileid)
                share = Share.objects.create(file_id=fileid, type=type, path=file.path, share_no=random_str)
        elif type == "radio":
            for fileid in fileids:
                print(str(fileid) + type + random_str)
                file = Radio.objects.get(file_id=fileid)
                share = Share.objects.create(file_id=fileid, type=type, path=file.path, share_no=random_str)
        elif type == "video":
            for fileid in fileids:
                print(str(fileid) + type + random_str)
                file = Video.objects.get(file_id=fileid)
                share = Share.objects.create(file_id=fileid, type=type, path=file.path, share_no=random_str)
        response.code = "200"
        response.msg = "ok"
        response.data = random_str
        return JsonResponse(response.dict)
        # except Exception as e:
        # print(e)
        # response.code = "500"
        # response.msg = "error!"
        # response.data = "null"
        # return JsonResponse(response.dict)


class ShareShowFile(APIView):
    def get(self, request):
        response = BaseResponse()
        try:
            shareno = request.query_params.dict()["shareno"]
            data = []
            share_list = Share.objects.filter(share_no=shareno)
            if share_list.exists():
                share_list = ShareSerializer(share_list, many=True)
                for share in share_list.data:
                    data.append(share)
                response.data = data
                response.code = "200"
                response.msg = "ok"
                return JsonResponse(response.dict)
            else:
                response.data = "empty!"
                response.code = "500"
                response.msg = "ok"
                return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "500"
            response.msg = "error!"
            response.data = "null"
            return JsonResponse(response.dict)


class ShareSaveFile(APIView):
    def post(self, request):
        response = BaseResponse()
        try:
            # data = request.data
            # userid = request.data.get('userid')
            userid = request.session['userid']
            #type = request.data.get('type')
            type = data['data']['type']
            # fileids = request.data.get('fileids')
            fileids = data['data']['fileids']
            #shareno = request.data.get('shareno')
            shareno = data['data']['shareno']
            if type == "img":
                for fileid in fileids:
                    print(str(fileid) + type + shareno + str(userid))
                    file = Img.objects.get(file_id=fileid)
                    # 自己不能给自己传 并且 自己名下不能有重名文件
                    if file.user_id == userid or Img.objects.get(filename=file.filename, user_id=userid):
                        response.code = "500"
                        response.msg = "exits!"
                        response.data = fileids
                        return JsonResponse(response.dict)
                    else:
                        Img.objects.create(filename=file.filename, type=file.type, size=file.size, path=file.path,
                                           user_id=userid, md5_id=file.md5_id)
                        Share.objects.filter(share_no=shareno, file_id=fileid).delete()
                        del fileids[0]
            elif type == "doc":
                for fileid in fileids:
                    print(str(fileid) + type + shareno + str(userid))
                    file = Doc.objects.get(file_id=fileid)
                    if file.user_id == userid or Doc.objects.get(filename=file.filename, user_id=userid):
                        response.code = "500"
                        response.msg = "exits!"
                        response.data = fileids
                        return JsonResponse(response.dict)
                    else:
                        Doc.objects.create(filename=file.filename, type=type, size=file.size, path=file.path,
                                           user_id=userid, md5_id=file.md5_id)
                        Share.objects.filter(share_no=shareno, file_id=fileid).delete()
                        del fileids[0]
            elif type == "radio":
                for fileid in fileids:
                    print(str(fileid) + type + shareno + str(userid))
                    file = Radio.objects.get(file_id=fileid)
                    if file.user_id == userid or Radio.objects.get(filename=file.filename, user_id=userid):
                        response.code = "500"
                        response.msg = "exits!"
                        response.data = fileids
                        return JsonResponse(response.dict)
                    else:
                        Radio.objects.create(filename=file.filename, type=type, size=file.size, path=file.path,
                                             user_id=userid, md5_id=file.md5_id)
                        Share.objects.filter(share_no=shareno, file_id=fileid).delete()
                        del fileids[0]
            elif type == "video":
                for fileid in fileids:
                    print(str(fileid) + type + shareno + str(userid))
                    file = Video.objects.get(file_id=fileid)
                    if file.user_id == userid:
                        response.code = "500"
                        response.msg = "exits!"
                        response.data = fileids
                        return JsonResponse(response.dict)
                    else:
                        Video.objects.create(filename=file.filename, type=type, size=file.size, path=file.path,
                                             user_id=userid, md5_id=file.md5_id)
                        Share.objects.filter(share_no=shareno, file_id=fileid).delete()
                        del fileids[0]
            response.data = "null"
            response.code = "200"
            response.msg = "ok"
            return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "500"
            response.msg = "error!"
            response.data = "null"
            return JsonResponse(response.dict)
