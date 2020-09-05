from django.http import Http404
from rest_framework import status, permissions, filters,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Event, Pledge, Category, Region
from .serializers import EventSerializer, PledgeSerializer, EventDetailSerializer, CategorySerializer, RegionSerializer
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly, IsSuperUserOrReadOnly
from rest_framework.generics import ListAPIView





class EventList(ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ['date_created']

    def get_queryset(self):
        queryset = Event.objects.all()
        category = self.request.query_params.get('category__name', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset

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
            event = Event.objects.get(slug=slug)
            self.check_object_permissions(self.request, event)
            return event
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
            pledge = Pledge.objects.get(pk=pk)
            self.check_object_permissions(self.request, pledge)
            return pledge
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
    permission_classes = [ permissions.IsAuthenticatedOrReadOnly]
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,permissions.IsAdminUser]

    def get_object(self, slug):
        try:
            category = Category.objects.get(slug=slug)
            self.check_object_permissions(self.request, category)
            return category
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        category = self.get_object(slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, slug):
        category = self.get_object(slug)
        serializer = CategorySerializer(
            instance = category,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, slug):
            category = self.get_object(slug)
            category.delete()
            return Response(status=status.HTTP_200_OK)

class RegionList(APIView):
    permission_classes = [ permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = RegionSerializer(data=request.data)
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

class RegionDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,permissions.IsAdminUser]

    def get_object(self, slug):
        try:
            region = Region.objects.get(slug=slug)
            self.check_object_permissions(self.request, region)
            return region
        except Region.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        region = self.get_object(slug)
        serializer = RegionSerializer(region)
        return Response(serializer.data)

    def put(self, request, slug):
        region = self.get_object(slug)
        serializer = RegionSerializer(
            instance = region,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, slug):
        region = self.get_object(slug)
        region.delete()
        return Response(status=status.HTTP_200_OK)