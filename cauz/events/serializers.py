from rest_framework import serializers
from .models import Event, Pledge

class EventSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=None)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    # owner = serializers.CharField(max_length=200)
    owner = serializers.ReadOnlyField(source='owner.id')

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

class PledgeSerializer(serializers.Serializer):
    id= serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField()
    supporter = serializers.CharField(max_length=200)
    event_id = serializers.IntegerField()

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data) 
class DetailEventSerializer(EventSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)



