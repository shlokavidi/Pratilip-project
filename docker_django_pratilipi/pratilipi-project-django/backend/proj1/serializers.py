from rest_framework import serializers
from .models import proj1

class Proj1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Proj1
        fields = ('id', 'title', 'description', 'completed')

