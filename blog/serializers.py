from rest_framework import serializers
from .models import Post, Comment, Category, Tag


class PublicPostSerializer(serializers.ModelSerializer):
    author  = serializers.ReadOnlyField(source='author.username')
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    tags = serializers.SlugRelatedField(read_only=True, slug_field='name', many=True)

    class Meta:
        model = Post
        fields = ['author', 'title', 'slug', 'content', 'image', 'category', 'tags', 'updated_at']
        extra_kwargs = {
            'slug':{'read_only':True},
        }


class UserPostSerilaizer(serializers.ModelSerializer):
    author  = serializers.ReadOnlyField(source='author.username')
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    tags = serializers.SlugRelatedField(read_only=True, slug_field='name', many=True)

    class Meta:
        model = Post
        fields = ['author', 'title', 'slug', 'content', 'image', 'category', 'tags', 'updated_at', 'created_at', 'is_published']
        extra_kwargs = {
            'updated_at':{'read_only':True},
            'created_at':{'read_only':True},
            'is_published':{'read_only':True},
            'author':{'read_only':True},
            'slug':{'read_only':True},
        }

    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.slug = None
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance    