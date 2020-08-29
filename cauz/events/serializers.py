from rest_framework import serializers
from .models import Event, Pledge, Category


class CategorySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=32)
    slug = serializers.CharField(required=False)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

class EventSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=None)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()     
    slug = serializers.CharField(required=False)
    # owner = serializers.CharField(max_length=200)
    owner = serializers.ReadOnlyField(source='owner.id')
    category = serializers.ReadOnlyField(source='Category', default='Charity')

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

class PledgeSerializer(serializers.Serializer):
    id= serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField()
    # supporter = serializers.CharField(max_length=200)
    supporter = serializers.ReadOnlyField(source='supporter.id')
    event = serializers.PrimaryKeyRelatedField(source='event.id',queryset=Event.objects.all())

    def create(self, validated_data):
        print(validated_data)
        # event=Event.objects.get(pk=validated_data['event'].id)
        
        return Pledge.objects.create(
            event=validated_data['event']['id'],
            amount=validated_data['amount'],
            anonymous=validated_data['anonymous'],
            supporter=validated_data['supporter']
        ) 

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.anonymous = validated_data.get('anonymous', instance.anonymous)
        instance.save()
        return instance

class EventDetailSerializer(EventSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance