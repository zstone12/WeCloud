from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
# Create your views here.
from rest_framework.views import APIView
from django.http import request
from rest_framework.response import Response
from api.serializers import  *
from api.models import  *
import hashlib
from collections import OrderedDict
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
        email = request.query_params.dict()["email"]
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
         user = User.objects.get(username=username, password=md5(password))
         userid=user.user_id
         print(user)
         if user:
             request.session['login'] = True
             request.session['userid']=user.user_id
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
                userid=request.session['userid']
                user=User.objects.get(user_id=userid)
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
                del request.session['userid']
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
            userid = request.session['userid']
            password = request.query_params.dict()["password"]
            user = User.objects.filter(user_id=userid, password=md5(password))
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


class GetFile(APIView):
    def get(self,request):
        response = BaseResponse()
        try:

            userid = request.session['userid']
            data = []
            if userid:
                type = request.query_params.dict()["type"]
                if type=="img":
                    img_list=Img.objects.filter(user_id=userid)
                    img_list=ImgSerializer(img_list,many=True)
                    data.append(img_list.data)
                    response.data=data
                elif type=="doc":
                    doc_list=Doc.objects.filter(user_id=userid)
                    doc_list=DocSerializer(doc_list,many=True)
                    data.append(doc_list.data)
                    response.data=data
                elif type=="radio":
                    radio_list=Radio.objects.filter(user_id=userid)
                    radio_list=RadioSerializer(radio_list,many=True)
                    data.append(radio_list.data)
                    response.data=data
                elif type=="video":
                    video_list=Video.objects.filter(user_id=userid)
                    video_list=VideoSerializer(video_list,many=True)
                    data.append(video_list.data)
                    response.data=data
                elif type=="all":
                    img_list=Img.objects.filter(user_id=userid)
                    doc_list = Doc.objects.filter(user_id=userid)
                    radio_list = Radio.objects.filter(user_id=userid)
                    video_list = Video.objects.filter(user_id=userid)

                    img_list=ImgSerializer(img_list,many=True)
                    doc_list=DocSerializer(doc_list,many=True)
                    radio_list=RadioSerializer(radio_list,many=True)
                    video_list=VideoSerializer(video_list,many=True)
                    data.append(img_list.data)
                    data.append(doc_list.data)
                    data.append(radio_list.data)
                    data.append(video_list.data)
                    if all=={}:
                        response.data = "null"
                    else:
                        response.data = data

                elif type=="trash":
                    trash_list=Trash.objects.filter(user_id=userid)
                    trash_list=TrashSerializer(trash_list,many=True)
                    data.append(trash_list.data)
                    response.data=data
                response.code = "200"
                response.msg = "ok"
                return JsonResponse(response.dict)
        except Exception as e:
              print(e)
              response.code = "201"
              response.msg = "no"
              response.data = "null"
              return JsonResponse(response.dict)


class GetNodeList:
    def get(self,request):
        response = BaseResponse()
        try:
            userid = request.session['userid']
            if userid:
                note_list=Note.objects.filter(user_id=userid)
                data=NoteSerializer(note_list,many=True).data
                response.code = "200"
                response.msg = "yes"
                response.data = data

            else:
                response.code = "201"
                response.msg = "no"
                response.data = "null"
        except:
            response.code = "201"
            response.msg = "no"
            response.data = "null"
        return JsonResponse(response.dict)


class GetNode:
    def get(self,request):
        response = BaseResponse()
        try:
            file_id=request.query_params.dict()['file_id']
            userid = request.session['userid']
            if userid:
                note=Note.objects.get(user_id=userid,file_id=file_id)
                data=NoteSerializer(note).data
                response.code = "200"
                response.msg = "yes"
                response.data = data

            else:
                response.code = "201"
                response.msg = "no"
                response.data = "null"
        except:
            response.code = "201"
            response.msg = "no"
            response.data = "null"
        return JsonResponse(response.dict)


class DelNode:
    def get(self,request):
        response = BaseResponse()
        try:
            file_id=request.query_params.dict()['file_id']
            userid = request.session['userid']
            if userid:
                Note.objects.get(user_id=userid,file_id=file_id).delete()
                note_list=Note.objects.all()
                data=NoteSerializer(note_list,many=True).data
                response.code = "200"
                response.msg = "yes"
                response.data = data

            else:
                response.code = "201"
                response.msg = "no"
                response.data = "null"
        except:
            response.code = "201"
            response.msg = "no"
            response.data = "null"
        return JsonResponse(response.dict)


class InsertNode:
    def post(self,request):
        response = BaseResponse()
        try:
            file_id=request.query_params.dict()['file_id']
            userid = request.session['userid']
            if userid:
                title=request.POST.get("title")
                content=request.POST.get("content")
                date=request.POST.get('date')
                data=Note.objects.get(user_id=userid,file_id=file_id)
                data.title=title
                data.content=content
                data.date=date
                data.save()
                note_list=Note.objects.all()
                data=NoteSerializer(note_list,many=True).data
                response.code = "200"
                response.msg = "yes"
                response.data = data

            else:
                title = request.POST.get("title")
                content = request.POST.get("content")
                date = request.POST.get('date')
                Note.objects.create(title=title,content=content,date=date,user_id=userid)
                note_list = Note.objects.all()
                data = NoteSerializer(note_list, many=True).data
                response.code = "200"
                response.msg = "yes"
                response.data = data
        except:
            response.code = "201"
            response.msg = "no"
            response.data = "null"
        return JsonResponse(response.dict)