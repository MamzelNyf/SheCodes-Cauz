from django.http import Http404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Event, Pledge, Category
from.serializers import EventSerializer, PledgeSerializer, EventDetailSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly

class EventList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class EventDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly]

    def get_object(self, slug):
        try:
            self.check_object_permissions(self.request, Event)
            return Event.objects.get(slug=slug)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        event = self.get_object(slug)
        serializer = EventDetailSerializer(event)
        return Response(serializer.data)

    def put(self, request, slug):
        event = self.get_object(slug)
        serializer = EventDetailSerializer(
            instance = event,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, slug):
            event = self.get_object(slug)
            event.delete()
            return Response(status=status.HTTP_200_OK)

class PledgeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self,request):
        print(request.data)
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class PledgeDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSupporterOrReadOnly]

    def get_object(self, pk):
        try:
            self.check_object_permissions(self.request, Pledge)
            return Pledge.objects.get(pk=pk)
        except Pledge.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeSerializer(pledge)
        return Response(serializer.data)

    def put(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeSerializer(
            instance = pledge,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
            pledge = self.get_object(pk)
            pledge.delete()
            return Response(status=status.HTTP_200_OK)

class CategoryList(APIView):
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class CategoryDetail(APIView):
    def get_object(self, slug):
        try:
            return Category.objects.get(slug=slug)
        except Pledge.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        category = self.get_object(slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)