from rest_framework import serializers
from api import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Img
        fields = '__all__'


class DocSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Doc
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Note
        fields = '__all__'


class RadioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Radio
        fields = '__all__'



class TrashSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trash
        fields = '__all__'


class CofferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coffer
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Video
        fields = '__all__'