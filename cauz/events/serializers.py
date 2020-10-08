from rest_framework import serializers
from .models import Event, Pledge, Category, Region


class CategorySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=32)
    slug = serializers.ReadOnlyField(required=False)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.save()
        return instance


class RegionSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=200)
    slug = serializers.CharField(required=False)

    def create(self, validated_data):
        return Region.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.save()
        return instance


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
    owner = serializers.ReadOnlyField(source="owner.username")
    # category = serializers.ReadOnlyField(source="Category", default="Charity")
    category = serializers.SlugRelatedField('name', queryset=Category.objects.all())
    # region = serializers.ReadOnlyField(source="Region", default="World")
    region = serializers.SlugRelatedField('name', queryset=Region.objects.all())


    def create(self, validated_data):
        return Event.objects.create(**validated_data)


class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField(max_length=200, allow_blank=True)
    anonymous = serializers.BooleanField()
    supporter = serializers.ReadOnlyField(source="supporter.username")
    event = serializers.PrimaryKeyRelatedField(
        source="event.id", queryset=Event.objects.all()
    )
    print("Pledge serialiser")

    def create(self, validated_data):
        print(validated_data)
        # event=Event.objects.get(pk=validated_data['event'].id)

        return Pledge.objects.create(
            event=validated_data["event"]["id"],
            amount=validated_data["amount"],
            comment=validated_data["comment"],
            anonymous=validated_data["anonymous"],
            supporter=validated_data["supporter"],
        )

    def update(self, instance, validated_data):
        instance.amount = validated_data.get("amount", instance.amount)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.anonymous = validated_data.get("anonymous", instance.anonymous)
        instance.save()
        return instance


class EventDetailSerializer(EventSerializer):
    pledges = PledgeSerializer(many=True, read_only=True, source="event_pledge")
    print("event serialiser")

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.goal = validated_data.get("goal", instance.goal)
        instance.image = validated_data.get("image", instance.image)
        instance.is_open = validated_data.get("is_open", instance.is_open)
        instance.date_created = validated_data.get(
            "date_created", instance.date_created
        )
        instance.owner = validated_data.get("owner", instance.owner)
        instance.category = validated_data.get("category", instance.category)
        instance.region = validated_data.get("region", instance.region)

        instance.save()
        return instance