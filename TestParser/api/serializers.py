from rest_framework import serializers

from news.models import Tag, News


class TagSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'resource', 'body', 'created_at', 'tags')
        read_only_fields = ('id', 'title', 'resource', 'body', 'created_at',)

