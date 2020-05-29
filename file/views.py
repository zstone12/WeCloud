from django.http import HttpResponse, JsonResponse, FileResponse
# Create your views here.
from rest_framework.views import APIView
from api.serializers import *
from api.models import *
import hashlib
from rest_framework.parsers import MultiPartParser
import hashlib
import datetime
import os


def getHash(f):
    line = f.readline()
    hash = hashlib.md5()
    while (line):
        hash.update(line)
        line = f.readline()
    return hash.hexdigest()


# Create your views here.
class BaseResponse(object):
    def __init__(self):
        self.code = 200
        self.msg = ""
        self.data = None

    @property
    def dict(self):
        return self.__dict__


class UpFile(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request):
        response = BaseResponse()
        try:
            user_id = request.session['userid']
            # user_id = request.query_params.dict()["user_id"]
            filename = request.query_params.dict()["filename"]
            response.code = "200"
            response.msg = "ok"
            if user_id:
                type = request.query_params.dict()["type"]
                if type == "img":
                    img_list = Img.objects.filter(user_id=user_id, filename=filename)
                    if img_list:
                        response.code = "201"
                        response.msg = 'no'
                elif type == "doc":
                    doc_list = Doc.objects.filter(user_id=user_id, filename=filename)
                    if doc_list:
                        response.code = "201"
                        response.msg = 'no'
                elif type == "radio":
                    radio_list = Radio.objects.filter(user_id=user_id, filename=filename)
                    if radio_list:
                        response.code = "201"
                        response.msg = 'no'
                elif type == "video":
                    video_list = Video.objects.filter(user_id=user_id, filename=filename)
                    if video_list:
                        response.code = "201"
                        response.msg = 'no'
                elif type == "coffer":
                    coffer_list = Coffer.objects.filter(user_id=user_id, filename=filename)
                    if coffer_list:
                        response.code = "201"
                        response.msg = 'no'
                return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.msg = 'no'
            response.code = '201'
            response.data = ""
            return JsonResponse(response.dict)

    def post(self, request):
        response = BaseResponse()
        try:
            type = request.data.get("type")
            # user_id = request.session['userid']
            user_id = request.data.get('user_id')
            filename = request.data.get("filename")
            file = request.FILES.getlist("file")
            for afile in file:
                md5 = getHash(afile)
                response.code = "201"
                response.msg = "no"
                if type == 'img':
                    if Img.objects.filter(filename=filename, md5_id=md5).count():
                        file_path = Img.objects.filter(filename=filename, md5_id=md5).first().path
                        Img.objects.create(filename=filename, md5_id=md5, user_id=user_id, path=file_path, type=type,
                                           size=len(file),
                                           date=datetime.datetime.now())
                    else:
                        Md5.objects.create(md5=md5, filename=filename)
                        Img.objects.create(filename=filename, md5_id=md5, user_id=user_id,
                                           path=request.FILES.get('file'), type=type,
                                           size=len(file),
                                           date=datetime.datetime.now())
                    response.code = "200"
                    response.msg = "ok"
                    response.data = "null"

                elif type == 'doc':
                    if Doc.objects.filter(filename=filename, md5_id=md5).count():
                        file_path = Doc.objects.filter(filename=filename, md5_id=md5).first().path
                        Doc.objects.create(filename=filename, md5_id=md5, user_id=user_id, path=file_path, type=type,
                                           size=len(file),
                                           date=datetime.datetime.now())
                    else:
                        Md5.objects.create(md5=md5, filename=filename)
                        Doc.objects.create(filename=filename, md5_id=md5, user_id=user_id,
                                           path=request.FILES.get('file'), type=type,
                                           size=len(file),
                                           date=datetime.datetime.now())
                    response.code = "200"
                    response.msg = "ok"
                    response.data = "null"

                elif type == 'radio':
                    if Radio.objects.filter(filename=filename, md5_id=md5).count():
                        file_path = Radio.objects.filter(filename=filename, md5_id=md5).first().path
                        Radio.objects.create(filename=filename, md5_id=md5, user_id=user_id, path=file_path, type=type,
                                             size=len(file),
                                             date=datetime.datetime.now())
                    else:
                        Md5.objects.create(md5=md5, filename=filename)
                        Radio.objects.create(filename=filename, md5_id=md5, user_id=user_id,
                                             path=request.FILES.get('file'), type=type,
                                             size=len(file),
                                             date=datetime.datetime.now())
                    response.code = "200"
                    response.msg = "ok"
                    response.data = "null"
                elif type == 'video':
                    if Video.objects.filter(filename=filename, md5_id=md5).count():
                        file_path = Video.objects.filter(filename=filename, md5_id=md5).first().path
                        Video.objects.create(filename=filename, md5_id=md5, user_id=user_id, path=file_path, type=type,
                                             size=len(file),
                                             date=datetime.datetime.now())
                    else:
                        Md5.objects.create(md5=md5, filename=filename)
                        Video.objects.create(filename=filename, md5_id=md5, user_id=user_id,
                                             path=request.FILES.get('file'), type=type,
                                             size=len(file),
                                             date=datetime.datetime.now())
                    response.code = "200"
                    response.msg = "ok"
                    response.data = "null"

                # elif type == 'coffer':
                #     if Coffer.objects.filter(filename=filename, md5_id=md5).count():
                #         file_path = Coffer.objects.filter(filename=filename, md5_id=md5).first().path
                #         Coffer.objects.create(filename=filename, md5_id=md5, user_id=user_id, path=file_path, type=type,
                #                               size=len(file),
                #                               date=datetime.datetime.now())
                #     else:
                #         Md5.objects.create(md5=md5, filename=filename)
                #         Coffer.objects.create(filename=filename, md5_id=md5, user_id=user_id,
                #                               path=request.FILES.get('file'), type=type,
                #                               size=len(file),
                #                               date=datetime.datetime.now())
                #     response.code = "200"
                #     response.msg = "ok"
                #     response.data = "null"
                return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.msg = 'no'
            response.code = '201'
            response.data = "null"
            return JsonResponse(response.dict)


class FileDownload(APIView):
    def post(self, request):
        response = BaseResponse()
        type = request.data.get("type")
        user_id = request.session['userid']
        filename = request.data.get("filename")
        # user_id = request.data.get("user_id")
        try:
            if type == "img":
                file_path = Img.objects.filter(user_id=user_id, filename=filename).first().path
                file = open(str(file_path), 'rb')
                file_response = FileResponse(file)
                file_response['Content-Type'] = 'application/octet-stream'
                file_response['Content-Disposition'] = filename
                file_response['code'] = "200"
                file_response['msg'] = "ok"
                return file_response
            elif type == "doc":
                file_path = Doc.objects.filter(user_id=user_id, filename=filename).first().path
                file = open(str(file_path), 'rb')
                file_response = FileResponse(file)
                file_response['Content-Type'] = 'application/octet-stream'
                file_response['Content-Disposition'] = filename
                file_response['code'] = "200"
                file_response['msg'] = "ok"
                return file_response
            elif type == "radio":
                file_path = Radio.objects.filter(user_id=user_id, filename=filename).first().path
                file = open(str(file_path), 'rb')
                file_response = FileResponse(file)
                file_response['Content-Type'] = 'application/octet-stream'
                file_response['Content-Disposition'] = filename
                file_response['code'] = "200"
                file_response['msg'] = "ok"
                return file_response
            elif type == "video":
                file_path = Video.objects.filter(user_id=user_id, filename=filename).first().path
                file = open(str(file_path), 'rb')
                file_response = FileResponse(file)
                file_response['Content-Type'] = 'application/octet-stream'
                file_response['Content-Disposition'] = filename
                file_response['code'] = "200"
                file_response['msg'] = "ok"
                return file_response
            # elif type == "coffer":
            #     file_path = Coffer.objects.filter(user_id=user_id, filename=filename).first().path
            #     file = open(str(file_path), 'rb')
            #     file_response = FileResponse(file)
            #     file_response['Content-Type'] = 'application/octet-stream'
            #     file_response['Content-Disposition'] = filename
            #     file_response['code'] = "200"
            #     file_response['msg'] = "ok"
            #     return file_response
            elif type == "trash":
                file_path = Trash.objects.filter(user_id=user_id, filename=filename).first().path
                file = open(str(file_path), 'rb')
                file_response = FileResponse(file)
                file_response['Content-Type'] = 'application/octet-stream'
                file_response['Content-Disposition'] = filename
                file_response['code'] = "200"
                file_response['msg'] = "ok"
                return file_response
        except Exception as e:
            print(e)
            response.msg = 'no'
            response.code = '201'
            response.data = "null"
            return JsonResponse(response.dict)


class GetFileByTime(APIView):
    def get(self, request):
        response = BaseResponse()
        try:
            data = []
            user_id = request.session['userid']
            # user_id = request.query_params.dict()["user_id"]
            if user_id:
                type = request.query_params.dict()["type"]
                if type == "img":
                    img_list = Img.objects.filter(user_id=user_id).order_by('-date')
                    img_list = ImgSerializer(img_list, many=True)
                    data.append(img_list.data)
                    response.data = data
                elif type == "doc":
                    doc_list = Doc.objects.filter(user_id=user_id).order_by('-date')
                    doc_list = DocSerializer(doc_list, many=True)
                    data.append(doc_list.data)
                    response.data = data
                elif type == "radio":
                    radio_list = Radio.objects.filter(user_id=user_id).order_by('-date')
                    radio_list = RadioSerializer(radio_list, many=True)
                    data.append(radio_list.data)
                    response.data = data
                elif type == "video":
                    video_list = Video.objects.filter(user_id=user_id).order_by('-date')
                    video_list = VideoSerializer(video_list, many=True)
                    data.append(video_list.data)
                    response.data = data
                elif type == "coffer":
                    coffer_list = Coffer.objects.filter(user_id=user_id).order_by('-date')
                    coffer_list = CofferSerializer(coffer_list, many=True)
                    data.append(coffer_list.data)
                    response.data = data
                elif type == "all":
                    img_list = Img.objects.filter(user_id=user_id).order_by('-date')
                    doc_list = Doc.objects.filter(user_id=user_id).order_by('-date')
                    radio_list = Radio.objects.filter(user_id=user_id).order_by('-date')
                    video_list = Video.objects.filter(user_id=user_id).order_by('-date')

                    img_list = ImgSerializer(img_list, many=True)
                    doc_list = DocSerializer(doc_list, many=True)
                    radio_list = RadioSerializer(radio_list, many=True)
                    video_list = VideoSerializer(video_list, many=True)
                    data.append(img_list.data)
                    data.append(doc_list.data)
                    data.append(radio_list.data)
                    data.append(video_list.data)
                    if all == {}:
                        response.data = "null"
                    else:
                        response.data = data

                elif type == "trash":
                    trash_list = Trash.objects.filter(user_id=user_id).order_by('-date')
                    trash_list = TrashSerializer(trash_list, many=True)
                    data.append(trash_list.data)
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


class InsertCoffer(APIView):
    def get(self, request):
        response = BaseResponse()
        try:
            type = request.query_params.dict()["type"]
            user_id = request.session['userid']
            filename = request.query_params.dict()["filename"]
            data = []
            if user_id:
                if type == "img":
                    file_path = Img.objects.filter(filename=filename, user_id=user_id).first().path
                    file_mad5 = Img.objects.filter(filename=filename, user_id=user_id).first().md5_id
                    file_size = Img.objects.filter(filename=filename, user_id=user_id).first().size
                    Coffer.objects.create(size=file_size, user_id=user_id, path=file_path, filename=filename,
                                          md5_id=file_mad5, date=datetime.datetime.now(), type=type)
                    coffer_list = Coffer.objects.all()
                    coffer_list = CofferSerializer(coffer_list, many=True)
                    data.append(coffer_list.data)
                    response.data = data
                elif type == "doc":
                    file_path = Doc.objects.filter(filename=filename, user_id=user_id).first().path
                    file_mad5 = Doc.objects.filter(filename=filename, user_id=user_id).first().md5_id
                    file_size = Doc.objects.filter(filename=filename, user_id=user_id).first().size
                    Coffer.objects.create(size=file_size, user_id=user_id, path=file_path, filename=filename,
                                          md5_id=file_mad5, date=datetime.datetime.now(), type=type)
                    coffer_list = Coffer.objects.all()
                    coffer_list = CofferSerializer(coffer_list, many=True)
                    data.append(coffer_list.data)
                    response.data = data
                elif type == "radio":
                    file_path = Radio.objects.filter(filename=filename, user_id=user_id).first().path
                    file_mad5 = Radio.objects.filter(filename=filename, user_id=user_id).first().md5_id
                    file_size = Radio.objects.filter(filename=filename, user_id=user_id).first().size
                    Coffer.objects.create(size=file_size, user_id=user_id, path=file_path, filename=filename,
                                          md5_id=file_mad5, date=datetime.datetime.now(), type=type)
                    coffer_list = Coffer.objects.all()
                    coffer_list = CofferSerializer(coffer_list, many=True)
                    data.append(coffer_list.data)
                    response.data = data
                elif type == "video":
                    file_path = Video.objects.filter(filename=filename, user_id=user_id).first().path
                    file_mad5 = Video.objects.filter(filename=filename, user_id=user_id).first().md5_id
                    file_size = Video.objects.filter(filename=filename, user_id=user_id).first().size
                    Coffer.objects.create(size=file_size, user_id=user_id, path=file_path, filename=filename,
                                          md5_id=file_mad5, date=datetime.datetime.now(), type=type)
                    coffer_list = Coffer.objects.all()
                    coffer_list = CofferSerializer(coffer_list, many=True)
                    data.append(coffer_list.data)
                    response.data = data
                elif type == "note":
                    file_path = Note.objects.filter(filename=filename, user_id=user_id).first().path
                    file_mad5 = Note.objects.filter(filename=filename, user_id=user_id).first().md5_id
                    file_size = Note.objects.filter(filename=filename, user_id=user_id).first().size
                    Coffer.objects.create(size=file_size, user_id=user_id, path=file_path, filename=filename,
                                          md5_id=file_mad5, date=datetime.datetime.now(), type=type)
                    coffer_list = Coffer.objects.all()
                    coffer_list = CofferSerializer(coffer_list, many=True)
                    data.append(coffer_list.data)
                    response.data = data
                response.code = "200"
                response.msg = "ok"
                return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            return JsonResponse(response.dict)


class Restore(APIView):
    def get(self, request):
        response = BaseResponse()
        try:
            type = request.query_params.dict()["type"]
            user_id = request.session['userid']
            filename = request.query_params.dict()["filename"]
            Coffer.objects.filter(type=type, user_id=user_id, filename=filename).delete()
            response.code = "200"
            response.msg = "ok"
            return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            return JsonResponse(response.dict)


class delNote(APIView):
    def get(self, request):
        response = BaseResponse()
        data = []
        user_id = request.session['userid']
        try:
            file_id = request.query_params.dict()["file_id"]
            Note.objects.filter(file_id=file_id, user_id=user_id).delete()
            note_list = Note.objects.all()
            note_list = NoteSerializer(note_list)
            data.append(note_list.data)
            response.data = data
            response.code = "200"
            response.msg = "ok"
            return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            return JsonResponse(response.dict)


class GetList(APIView):
    def get(self, request):
        response = BaseResponse()
        user_id = request.session['userid']
        data = []
        try:
            note_list = Note.objects.filter(user_id)
            note_list = NoteSerializer(note_list)
            data.append(note_list.data)
            response.data = data
            response.code = "200"
            response.msg = "ok"
            return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            return JsonResponse(response.dict)


class InsertNote(APIView):
    def get(self, request):
        response = BaseResponse()
        data = []
        try:
            user_id = request.session['userid']
            file_id = request.query_params.dict()["file_id"]
            title = request.query_params.dict()["title"]
            content = request.query_params.dict()["content"]
            need = request.query_params.dict()["need"]
            if need == 'update':
                Note.objects.filter(file_id=file_id, user_id=user_id).update(title=title, content=content)
            elif need == 'insert':
                Note.objects.create(file_id=file_id, title=title, content=content, user_id=user_id,
                                    data=datetime.datetime.now())
            note_list = Note.objects.all()
            note_list = NoteSerializer(note_list)
            data.append(note_list.data)
            response.data = data
            response.code = "200"
            response.msg = "ok"
            return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            return JsonResponse(response.dict)


class GetNote(APIView):
    def get(self, request):
        response = BaseResponse()
        data = []
        try:
            file_id = request.query_params.dict()["file_id"]
            note_list = Note.objects.filter(file_id=file_id)
            note_list = NoteSerializer(note_list)
            data.append(note_list.data)
            response.data = data
            response.code = "200"
            response.msg = "ok"
            return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            return JsonResponse(response.dict)


class DeleteFile(APIView):
    def get(self, request):
        response = BaseResponse()
        try:
            user_id = request.session['userid']
            filename = request.query_params.dict()["filename"]
            type = request.query_params.dict()["type"]
            file_path = Trash.objects.filter(user_id=user_id, filename=filename, type=type).first().path
            Trash.objects.filter(user_id=user_id, filename=filename, type=type).delete()
            os.remove(str(file_path))
            response.code = "200"
            response.msg = "ok"
            return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            return JsonResponse(response.dict)


class GotoTrash(APIView):
    def get(self, request):
        response = BaseResponse()
        try:
            user_id = request.session['userid']
            filename = request.query_params.dict()["filename"]
            type = request.query_params.dict()["type"]
            if user_id:
                if type == 'img':
                    path = Img.objects.filter(user_id=user_id, filename=filename).first().path
                    date = Img.objects.filter(user_id=user_id, filename=filename).first().date
                    md5 = Img.objects.filter(user_id=user_id, filename=filename).first().md5_id
                    size = Img.objects.filter(user_id=user_id, filename=filename).first().size
                    Trash.objects.create(user_id=user_id, filename=filename, path=path, date=date, md5_id=md5,
                                         type=type, size=size)
                    Img.objects.filter(user_id=user_id, filename=filename).delete()
                elif type == 'doc':
                    path = Doc.objects.filter(user_id=user_id, filename=filename).first().path
                    date = Doc.objects.filter(user_id=user_id, filename=filename).first().date
                    md5 = Doc.objects.filter(user_id=user_id, filename=filename).first().md5_id
                    size = Doc.objects.filter(user_id=user_id, filename=filename).first().size
                    Trash.objects.create(user_id=user_id, filename=filename, path=path, date=date, md5_id=md5,
                                         type=type, size=size)
                    Doc.objects.filter(user_id=user_id, filename=filename).delete()
                elif type == 'video':
                    path = Video.objects.filter(user_id=user_id, filename=filename).first().path
                    date = Video.objects.filter(user_id=user_id, filename=filename).first().date
                    md5 = Video.objects.filter(user_id=user_id, filename=filename).first().md5_id
                    size = Video.objects.filter(user_id=user_id, filename=filename).first().size
                    Trash.objects.create(user_id=user_id, filename=filename, path=path, date=date, md5_id=md5,
                                         type=type, size=size)
                    Video.objects.filter(user_id=user_id, filename=filename).delete()
                elif type == 'radio':
                    path = Radio.objects.filter(user_id=user_id, filename=filename).first().path
                    date = Radio.objects.filter(user_id=user_id, filename=filename).first().date
                    md5 = Radio.objects.filter(user_id=user_id, filename=filename).first().md5_id
                    size = Radio.objects.filter(user_id=user_id, filename=filename).first().size
                    Trash.objects.create(user_id=user_id, filename=filename, path=path, date=date, md5_id=md5,
                                         type=type, size=size)
                    Radio.objects.filter(user_id=user_id, filename=filename).delete()
                response.code = "200"
                response.msg = "ok"
                return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            return JsonResponse(response.dict)


class HuiFu(APIView):
    def get(self, request):
        response = BaseResponse()
        try:
            user_id = request.session['userid']
            filename = request.query_params.dict()["filename"]
            type = request.query_params.dict()["type"]
            if user_id:
                path = Trash.objects.filter(user_id=user_id, filename=filename, type=type).first().path
                date = Trash.objects.filter(user_id=user_id, filename=filename).first().date
                md5 = Trash.objects.filter(user_id=user_id, filename=filename).first().md5_id
                size = Trash.objects.filter(user_id=user_id, filename=filename).first().size
                if type == 'img':
                    Img.objects.create(user_id=user_id, filename=filename, path=path, date=date, md5_id=md5,
                                       type=type, size=size)
                    Trash.objects.filter(user_id=user_id, filename=filename, type=type).delete()
                elif type == 'doc':
                    Doc.objects.create(user_id=user_id, filename=filename, path=path, date=date, md5_id=md5,
                                       type=type, size=size)
                    Trash.objects.filter(user_id=user_id, filename=filename, type=type).delete()
                elif type == 'radio':
                    Radio.objects.create(user_id=user_id, filename=filename, path=path, date=date, md5_id=md5,
                                         type=type, size=size)
                    Trash.objects.filter(user_id=user_id, filename=filename, type=type).delete()
                elif type == 'video':
                    Video.objects.create(user_id=user_id, filename=filename, path=path, date=date, md5_id=md5,
                                         type=type, size=size)
                    Trash.objects.filter(user_id=user_id, filename=filename, type=type).delete()
                response.code = "200"
                response.msg = "ok"
                return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            return JsonResponse(response.dict)
