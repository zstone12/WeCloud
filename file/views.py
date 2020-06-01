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


class GetList(APIView):
    def get(self, request):
        response = BaseResponse()
        user_id = request.session['userid']
        try:
            note_list = Note.objects.filter(user_id=user_id)
            note_list = NoteSerializer(note_list,many=True)
            response.data = note_list.data
            response.code = "200"
            response.msg = "ok"
            return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            return JsonResponse(response.dict)

class UpFile(APIView):
    parser_classes = (MultiPartParser,)
    # def get(self, request):
    #     response = BaseResponse()
    #     try:
    #         user_id = request.session['userid']
    #         # user_id = request.query_params.dict()["user_id"]
    #         filename = request.query_params.dict()["filename"]
    #         response.code = "200"
    #         response.msg = "ok"
    #         if user_id:
    #
    #             filetype = request.query_params.dict()["type"]
    #             if filetype == "img":
    #                 img_list = Img.objects.filter(user_id=user_id, filename=filename)
    #                 if img_list:
    #                     response.code = "201"
    #                     response.msg = 'no'
    #             elif filetype == "doc":
    #                 doc_list = Doc.objects.filter(user_id=user_id, filename=filename)
    #                 if doc_list:
    #                     response.code = "201"
    #                     response.msg = 'no'
    #             elif filetype == "radio":
    #                 radio_list = Radio.objects.filter(user_id=user_id, filename=filename)
    #                 if radio_list:
    #                     response.code = "201"
    #                     response.msg = 'no'
    #             elif filetype == "video":
    #                 video_list = Video.objects.filter(user_id=user_id, filename=filename)
    #                 if video_list:
    #                     response.code = "201"
    #                     response.msg = 'no'
    #
    #             return JsonResponse(response.dict)
    #     except Exception as e:
    #         print(e)
    #         response.msg = 'no'
    #         response.code = '201'
    #         response.data = "null"
    #         return JsonResponse(response.dict)

    def post(self, request):
        response = BaseResponse()
        try:
            img_list = ["jpg", "png", "img", "jpeg"]
            doc_list = ["doc", "docx", "txt","md"]
            video_list = ["mov", "flv", "mp4", "rmvb", "rm"]
            radio_list = ["mp3", "midi", "wma"]

            user_id = request.session['userid']
            # user_id = request.data.get('user_id')
            # filename = request.data.get("filename")
            file = request.FILES.getlist("file")
            print(file)
            for afile in file:
                filename=afile.name
                print(filename)
                filetype=afile.name.split(".")[-1]
                md5 = getHash(afile)
                response.code = "201"
                response.msg = "no"
                print(filetype)
                if filetype in img_list:
                    img_list = Img.objects.filter(user_id=user_id, filename=filename)
                    print(img_list)
                    if img_list:
                        response.code = "201"
                        response.msg = 'no'
                        return JsonResponse(response.dict)
                    if Md5.objects.filter(md5=md5).count():
                        file_path = Img.objects.filter(md5_id=md5).first().path
                        Img.objects.create(filename=filename, md5_id=md5, user_id=user_id, path=file_path, type="img",
                                           size=afile.size,
                                           date=datetime.datetime.now())
                    else:
                        Md5.objects.create(md5=md5, filename=filename)
                        Img.objects.create(filename=filename, md5_id=md5, user_id=user_id,
                                           path=request.FILES.get('file'), type="img",
                                           size=afile.size,
                                           date=datetime.datetime.now())
                    user = User.objects.get(user_id=user_id)
                    user.size = user.size - afile.size
                    user.save()
                    response.code = "200"
                    response.msg = "ok"
                    response.data = "null"

                elif filetype in doc_list:
                    doc_list = Doc.objects.filter(user_id=user_id, filename=filename)
                    if doc_list:
                        response.code = "201"
                        response.msg = 'no'
                        return  JsonResponse(response.dict)
                    if  Md5.objects.filter(md5=md5).count():
                        file_path = Doc.objects.filter(md5_id=md5).first().path
                        Doc.objects.create(filename=filename, md5_id=md5, user_id=user_id, path=file_path, type="doc",
                                           size=afile.size,
                                           date=datetime.datetime.now())
                    else:
                        Md5.objects.create(md5=md5, filename=filename)
                        Doc.objects.create(filename=filename, md5_id=md5, user_id=user_id,
                                           path=request.FILES.get('file'), type="doc",
                                           size=afile.size,
                                           date=datetime.datetime.now())
                    user = User.objects.get(user_id=user_id)
                    user.size = user.size - afile.size
                    user.save()
                    response.code = "200"
                    response.msg = "ok"
                    response.data = "null"

                elif filetype in radio_list:
                    radio_list = Radio.objects.filter(user_id=user_id, filename=filename)
                    if radio_list:
                        response.code = "201"
                        response.msg = 'no'
                        return JsonResponse(response.dict)
                    if Md5.objects.filter(md5=md5).count():
                        file_path = Radio.objects.filter(md5_id=md5).first().path
                        Radio.objects.create(filename=filename, md5_id=md5, user_id=user_id, path=file_path, type="radio",
                                             size=afile.size,
                                             date=datetime.datetime.now())
                    else:
                        Md5.objects.create(md5=md5, filename=filename)
                        Radio.objects.create(filename=filename, md5_id=md5, user_id=user_id,
                                             path=request.FILES.get('file'), type="radio",
                                             size=afile.size,
                                             date=datetime.datetime.now())
                    user = User.objects.get(user_id=user_id)
                    user.size = user.size - afile.size
                    user.save()
                    response.code = "200"
                    response.msg = "ok"
                    response.data = "null"
                elif filetype in video_list:
                    video_list = Video.objects.filter(user_id=user_id, filename=filename)
                    if video_list:
                        response.code = "201"
                        response.msg = 'no'
                        return JsonResponse(response.dict)
                    if  Md5.objects.filter(md5=md5).count():
                        file_path = Video.objects.filter(md5_id=md5).first().path
                        Video.objects.create(filename=filename, md5_id=md5, user_id=user_id, path=file_path, type="video",
                                             size=afile.size,
                                             date=datetime.datetime.now())
                    else:
                        Md5.objects.create(md5=md5, filename=filename)
                        Video.objects.create(filename=filename, md5_id=md5, user_id=user_id,
                                             path=request.FILES.get('file'), type="video",
                                             size=afile.size,
                                             date=datetime.datetime.now())
                    user = User.objects.get(user_id=user_id)
                    user.size = user.size - afile.size
                    user.save()
                    response.code = "200"
                    response.msg = "ok"
                    response.data = "null"

                return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.msg = 'no'
            response.code = '201'
            response.data = "null"
            return JsonResponse(response.dict)


class FileDownload(APIView):

    def get(self, request):
        response = BaseResponse()
        type = request.query_params.dict()["type"]
        user_id = request.session['userid']
        filename = request.query_params.dict()["filename"]
        # user_id = request.data.get("user_id")
        try:
            if type == "img":
                file_path = Img.objects.filter(user_id=user_id, filename=filename).first().path
                print(file_path)
                file = open('/home/ubuntu/WeCloud/files/'+str(file_path), 'rb')
                file_response = FileResponse(file)
                file_response['Content-Type'] = 'application/force-download'
                file_response['Content-Disposition'] = 'attachment;filename="'+filename+'"'


                return file_response
            elif type == "doc":
                file_path = Img.objects.filter(user_id=user_id, filename=filename).first().path
                file = open('/home/ubuntu/WeCloud/files/'+str(file_path), 'rb')
                file_response = FileResponse(file)
                file_response['Content-Type'] = 'application/octet-stream'
                file_response['Content-Disposition'] = 'attachment;filename="' + filename + '"'

                return file_response


            elif type == "radio":
                file_path = Img.objects.filter(user_id=user_id, filename=filename).first().path
                file = open('/home/ubuntu/WeCloud/files/'+str(file_path), 'rb')
                file_response = FileResponse(file)
                file_response['Content-Type'] = 'application/octet-stream'
                file_response['Content-Disposition'] = 'attachment;filename="' + filename + '"'

                return file_response


            elif type == "video":
                file_path = Img.objects.filter(user_id=user_id, filename=filename).first().path
                file = open('/home/ubuntu/WeCloud/files/'+str(file_path), 'rb')
                file_response = FileResponse(file)
                file_response['Content-Type'] = 'application/force-download'
                file_response['Content-Disposition'] = 'attachment;filename="' + filename + '"'


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
                file_path = Img.objects.filter(user_id=user_id, filename=filename).first().path
                file = open(str(file_path), 'rb')
                file_response = FileResponse(file)
                file_response['Content-Type'] = 'application/octet-stream'
                file_response['Content-Disposition'] = 'attachment;filename="' + filename + '"'


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
                    img_list = Img.objects.filter(user_id=user_id).order_by('-date')
                    doc_list = Doc.objects.filter(user_id=user_id).order_by('-date')
                    radio_list = Radio.objects.filter(user_id=user_id).order_by('-date')
                    video_list = Video.objects.filter(user_id=user_id).order_by('-date')

                    img_list = ImgSerializer(img_list, many=True)
                    doc_list = DocSerializer(doc_list, many=True)
                    radio_list = RadioSerializer(radio_list, many=True)
                    video_list = VideoSerializer(video_list, many=True)
                    for img in img_list.data:
                        data.append(img)
                    for doc in doc_list.data:
                        data.append(doc)
                    for radio in radio_list.data:
                        data.append(radio)
                    for video in video_list.data:
                        data.append(video)
                    if all == {}:
                        response.data = "null"
                    else:
                        response.data = data
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

                    Img.objects.filter(user_id=user_id, filename=filename).delete()
                elif type == "doc":
                    file_path = Doc.objects.filter(filename=filename, user_id=user_id).first().path
                    file_mad5 = Doc.objects.filter(filename=filename, user_id=user_id).first().md5_id
                    file_size = Doc.objects.filter(filename=filename, user_id=user_id).first().size
                    Coffer.objects.create(size=file_size, user_id=user_id, path=file_path, filename=filename,
                                          md5_id=file_mad5, date=datetime.datetime.now(), type=type)
                    Doc.objects.filter(user_id=user_id, filename=filename).delete()

                elif type == "radio":
                    file_path = Radio.objects.filter(filename=filename, user_id=user_id).first().path
                    file_mad5 = Radio.objects.filter(filename=filename, user_id=user_id).first().md5_id
                    file_size = Radio.objects.filter(filename=filename, user_id=user_id).first().size
                    Coffer.objects.create(size=file_size, user_id=user_id, path=file_path, filename=filename,
                                          md5_id=file_mad5, date=datetime.datetime.now(), type=type)
                    Radio.objects.filter(user_id=user_id, filename=filename).delete()
                elif type == "video":
                    file_path = Video.objects.filter(filename=filename, user_id=user_id).first().path
                    file_mad5 = Video.objects.filter(filename=filename, user_id=user_id).first().md5_id
                    file_size = Video.objects.filter(filename=filename, user_id=user_id).first().size
                    Coffer.objects.create(size=file_size, user_id=user_id, path=file_path, filename=filename,
                                          md5_id=file_mad5, date=datetime.datetime.now(), type=type)
                    Video.objects.filter(user_id=user_id, filename=filename).delete()
                coffer_list = Coffer.objects.all()
                coffer_list = CofferSerializer(coffer_list, many=True)

                response.data = coffer_list.data

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
            if type=="img":
                img=Coffer.objects.filter(user_id=user_id,filename=filename).first()
                Img.objects.create(filename=img.filename, md5_id=img.md5_id, user_id=user_id,
                                   path=img.path, type="img",
                                   size=img.size,
                                   date=img.date)
            elif type=="doc":
                doc= Coffer.objects.filter(user_id=user_id, filename=filename).first()
                Doc.objects.create(filename=doc.filename, md5_id=doc.md5_id, user_id=user_id,
                                   path=doc.path, type="doc",
                                   size=doc.size,
                                   date=doc.date)
            elif type=="video":
                video = Coffer.objects.filter(user_id=user_id, filename=filename).first()
                Video.objects.create(filename=video.filename, md5_id=video.md5_id, user_id=user_id,
                                   path=video.path, type="video",
                                   size=video.size,
                                   date=video.date)
            elif type=="radio":
                radio = Coffer.objects.filter(user_id=user_id, filename=filename).first()
                Radio.objects.create(filename=radio.filename, md5_id=radio.md5_id, user_id=user_id,
                                     path=radio.path, type="radio",
                                     size=radio.size,
                                     date=radio.date)
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
            note_list = Note.objects.filter(user_id=user_id)
            note_list = NoteSerializer(note_list,many=True)
            data=note_list.data
            response.data = data
            response.code = "200"
            response.msg = "ok"
            return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            return JsonResponse(response.dict)


class CreateNote(APIView):
    def get(self,request):
            response = BaseResponse()
            try:
                user_id = request.session['userid']
                if user_id:
                    current_time=datetime.datetime.now()
                    note=Note.objects.create(title="", content="", user_id=user_id,
                                        date=current_time)
                    response.code=200
                    response.msg="ok"

                    current_time = datetime.datetime.strftime(current_time,'%Y-%m-%d')
                    print(current_time)
                    data={
                        "file_id":note.file_id,
                        "date":current_time
                    }
                    response.data=data
                    return JsonResponse(response.dict)
            except Exception as e:
                    print(e)
                    response.code = 201
                    response.msg = "no"
                    response.data = "null"
                    return JsonResponse(response.dict)

class UpdateNote(APIView):

    def post(self, request):
        response = BaseResponse()
        data = []
        try:
            user_id = request.session['userid']
            file_id = request.data['data']["file_id"]
            title = request.data['data']['title']
            content = request.data['data']["content"]
            Note.objects.filter(file_id=file_id, user_id=user_id).update(title=title, content=content,date=datetime.datetime.now())

            note = Note.objects.get(file_id=file_id)
            note= NoteSerializer(note)
            data=note.data
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
            note_list = Note.objects.get(file_id=file_id)
            note_list = NoteSerializer(note_list)
            data=note_list.data
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
    def post(self, request):
        response = BaseResponse()
        try:
            user_id = request.session['userid']
            print(request.data)
            for filedata in request.data['data']['listData']:
              trash = Trash.objects.filter(user_id=user_id, filename=filedata['filename'],
                                             type=filedata['type']).first()
              file_path = trash.path
              if filedata['type']=="img":
                    count=Img.objects.filter(md5_id=trash.md5_id).count()
                    count+=Trash.objects.filter(md5_id=trash.md5_id).count()
                    if count==1:
                        os.remove("/home/ubuntu/WeCloud/files/"+file_path)
                        Md5.objects.filter(md5=trash.md5_id).delete()
              elif filedata['type']=="doc":
                  count = Doc.objects.filter(md5_id=trash.md5_id).count()
                  count += Trash.objects.filter(md5_id=trash.md5_id).count()
                  if count == 1:
                      os.remove("/home/ubuntu/WeCloud/files/" + file_path)
                      Md5.objects.filter(md5=trash.md5_id).delete()
              elif filedata['type']=="radio":
                  count = Radio.objects.filter(md5_id=trash.md5_id).count()
                  count += Trash.objects.filter(md5_id=trash.md5_id).count()
                  if count == 1:
                      os.remove("/home/ubuntu/WeCloud/files/" + file_path)
                      Md5.objects.filter(md5=trash.md5_id).delete()
              elif filedata['type']=="video":
                  count = Video.objects.filter(md5_id=trash.md5_id).count()
                  count += Trash.objects.filter(md5_id=trash.md5_id).count()
                  if count == 1:
                      os.remove("/home/ubuntu/WeCloud/files/" + file_path)
                      Md5.objects.filter(md5=trash.md5_id).delete()
              Trash.objects.filter(user_id=user_id, filename=filedata['filename'], type=filedata['type']).delete()
            response.code = "200"
            response.msg = "ok"
            return JsonResponse(response.dict)
        except Exception as e:
            print(e)
            response.code = "201"
            response.msg = "no"
            return JsonResponse(response.dict)


class GotoTrash(APIView):
    def post(self, request):
        response = BaseResponse()
        try:
            user_id = request.session['userid']
            files = request.data['data']['listData']
            for file in files:

                filename=file['filename']
                print('filename:'+filename)
                type=file['type']
                print('type:'+type)
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
    def post(self, request):
        response = BaseResponse()
        try:
            user_id = request.session['userid']
            files = request.data['data']['listData']
            for file in files:
                filename = file['filename']
                type = file['type']

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
