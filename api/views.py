from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
# Create your views here.
from rest_framework.views import APIView
from django.http import request
from rest_framework.response import Response
from api.serializers import  *
from api.models import  *
import hashlib

def md5(str):
    m1 = hashlib.md5()
    m1.update(str.encode(encoding='UTF-8'))
    token = m1.hexdigest()
    return token
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
        response.msg="ok"
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


class Reg(APIView):
    def post(self,request):
        response = BaseResponse()
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        try:
            obj = User.objects.create(username=username, password=md5(password), email=email)
            response.msg = 'ok'
            response.code = 200
            response.data="null"
        except Exception as e:
            print(e)
            response.msg = 'no'
            response.code = 201
            response.data = "null"

        return JsonResponse(response.dict)


class Login(APIView):
     def post(self,request):
         response = BaseResponse()
         username = request.data.get('username')
         password = request.data.get('password')
         user = User.objects.filter(username=username, password=md5(password))
         if user:
             request.session['login'] = True
             request.session['username']=username
             response.msg = "ok"
             response.data = "null"
         else:
                 response.msg = "no"
                 response.code = 201
                 response.data = "null"

         return JsonResponse(response.dict)


class IsLog(APIView):
      def get(self,request):
          response = BaseResponse()
          try:
            login=request.session['login']

            if login:
                username=request.session['username']
                print(username)
                user=User.objects.get(username=username)
                img_size = user.img_set.count()
                radio_size= user.radio_set.count()
                doc_size= user.doc_set.count()
                video_size = user.video_set.count()
                data={
                    'img':img_size,
                    'radio':radio_size,
                    'doc_size':doc_size,
                    'video_size':video_size
                }
                response.code="200"
                response.msg="ok"
                response.data=data
                return  JsonResponse(response.dict)
            else:
                response.code = "201"
                response.msg = "no"
                response.data = "null"
                return JsonResponse(response.dict)
          except Exception as e:

              response.code = "201"
              response.msg = "no"
              response.data = "null"
              return JsonResponse(response.dict)


class OutLogin(APIView):
        def get(self,request):
            response = BaseResponse()
            try:
                del request.session['login']
                del request.session['username']
                response.code = "200"
                response.msg = "yes"
                response.data = "null"
            except KeyError:
                response.code = "201"
                response.msg = "no"
                response.data = "null"
            return JsonResponse(response.dict)


class CheckPassword(APIView):
    def get(self,request):
        response = BaseResponse()
        try:
            username = request.session['username']
            password = request.query_params.dict()["password"]
            user = User.objects.filter(username=username, password=md5(password))
            if user:
                response.code = "200"
                response.msg = "ok"
                response.data = "null"
                return JsonResponse(response.dict)
            else:
                response.code = "201"
                response.msg = "no"
                response.data = "null"
                return JsonResponse(response.dict)

        except:
              response.code = "201"
              response.msg = "no"
              response.data = "null"
              return JsonResponse(response.dict)
