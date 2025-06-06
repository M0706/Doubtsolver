from rest_framework import serializers
from .models import DoubtEntry

class DoubtEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoubtEntry
        fields = '__all__' 