from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404

from . models import StreamPlatform, WatchList, Review
from . serializers import StreamPlatformSerializer, WatchListSerializer, ReviewSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.reverse import reverse


# Create your views here.
# 1. Function Based View

# def movie_list(request):
#     MovieList = WatchList.objects.all()
#     serialized = WatchListSerializer(MovieList, many=True)
#     return JsonResponse(serialized.data, safe=False)

def movie_detail(request, pk):
    movie = WatchList.objects.get(pk=pk)
    serialized = WatchListSerializer(movie)
    return JsonResponse(serialized.data, safe=False)

@api_view(['GET', 'POST'])
def movie_list(request, format=None):
    if request.method == 'GET':
        MovieList = WatchList.objects.all()
        serialized = WatchListSerializer(MovieList, many=True)
        return Response(serialized.data)

    elif request.method == 'POST':
        _data = request.data
        serialized = WatchListSerializer(data=_data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
def stream_list(request, format=None):
    if request.method == 'GET':
        StreamList = StreamPlatform.objects.all()
        serialized = StreamPlatformSerializer(StreamList, many=True)
        return Response(serialized.data)

    elif request.method == 'POST':
        _data = request.data
        serialized = StreamPlatformSerializer(data=_data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def stream_detail(request, pk, format=None):
    try:
        stream = StreamPlatform.objects.get(pk=pk)
    except StreamPlatform.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serialized = StreamPlatformSerializer(stream)
        return Response(serialized.data)

    elif request.method == 'PUT':
        _data = request.data
        serialized = StreamPlatformSerializer(data=_data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        stream.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 2. Class Based Views

class StreamPlatformList(APIView):
    """
        List all Stream Platform List, or create a new Stream Platform.
    """
    def get(self, request, format=None):
        StreamList = StreamPlatform.objects.all()
        serialized = StreamPlatformSerializer(StreamList, many=True)
        return Response(serialized.data)

    def post(self, request, format=None):
        _data = request.data
        serialized = StreamPlatformSerializer(data=_data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformDetails(APIView):
    """
       Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        stream = self.get_object(pk)
        serialized = StreamPlatformSerializer(stream)
        return Response(serialized.data)

    def put(self, request, pk, format=None):
        stream = self.get_object(pk)
        serialized = StreamPlatformSerializer(stream)
        if serialized.is_valid():
            serialized.save()
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        stream = self.get_object(pk)
        stream.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#  3. Using mixins

class StreamingPlatformsList(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                        generics.GenericAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class StreamingPlatformsDetails(mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                generics.GenericAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# 4. Using generic class-based views

class StreamingLists(generics.ListCreateAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


class StreamingDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

# 5. Hyperlinking our API

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'ClassMovieList': reverse('streamplatform-classlist', request=request, format=format),
        'MixingStreamList': reverse('streamplatform-mixinglist', request=request, format=format)
    })

class ReviewsListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewsDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


    