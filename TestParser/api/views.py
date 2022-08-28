import datetime

from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from news.models import Tag, News
from .parsers.parser import parse_news
from .serializers import TagSerializer, NewsSerializer


class TagsViewSet(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsViewSet(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags', 'created_at')

    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        queryset = self.filter_queryset(request, news)
        if queryset:
            serializer = NewsSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'detail': 'Records not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, *args, **kwargs):
        url = self.request.data['url']
        data = parse_news(url)
        for item in data:
            if not News.objects.filter(title=item['header']).exists():
                time = item['meta']
                news = News.objects.create(
                    title=item['header'],
                    body=item['description'],
                    created_at=time,
                    resource=url,
                )
                if item['tags'] is not None:
                    for tag_name in item['tags']:
                        try:
                            tag = Tag.objects.get(name=tag_name)
                        except ObjectDoesNotExist:
                            tag = Tag.objects.create(name=tag_name)
                        news.tags.add(tag)

        return Response(
                        {'detail': 'Records added successfully'},
                        status=status.HTTP_201_CREATED
                    )

    def filter_queryset(self, request, queryset):
        get_data = request.query_params
        if 'tags' in get_data and len(get_data) == 1:
            tags = get_data['tags']
            queryset = queryset.filter(tags__name=tags)
        elif 'created_at' in get_data and len(get_data) == 1:
            date = datetime.datetime.strptime(get_data['created_at'], '%Y-%m-%d')
            start_date = date.replace(hour=0, minute=0, second=0)
            end_date = date.replace(hour=23, minute=59, second=59)
            queryset = queryset.filter(created_at__range=(start_date, end_date))
        return queryset
