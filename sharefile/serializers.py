from rest_framework import serializers
from sharefile import models


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Share
        fields = '__all__'
