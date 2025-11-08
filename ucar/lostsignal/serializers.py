from rest_framework import serializers
from .models import Allert

class AllertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allert
        fields = ['id', 'description', 'status', 'source', 'create_time']
        read_only_fields = ['id', 'status', 'create_time']
