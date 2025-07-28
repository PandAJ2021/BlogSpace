from rest_framework import serializers
from .models import Post, Comment, PostLike, CommentLike


class ReadOnlyPostSerializer(serializers.ModelSerializer):
    author  = serializers.ReadOnlyField(source='author.username')
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    tags = serializers.SlugRelatedField(read_only=True, slug_field='name', many=True)
    likes_count = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ['author', 'title', 'slug', 'content', 'image', 'category', 'tags', 'updated_at', 'likes_count']
        read_only_fields = ['slug', 'likes_count']


class UserPostSerilaizer(serializers.ModelSerializer):
    author  = serializers.ReadOnlyField(source='author.username')
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    tags = serializers.SlugRelatedField(read_only=True, slug_field='name', many=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', 'slug', 'updated_at', 'created_at', 'is_published', 'likes_count']

    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.slug = None
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance    


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SlugRelatedField(read_only=True, slug_field='title')
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    comments = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ['post', 'user', 'content', 'created_at', 'comments', 'is_approved', 'likes_count']

    def get_comments(self, obj):
       children = obj.comments.filter(is_approved=True)
       return CommentSerializer(children, many=True).data


class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLike
        fields = ['user', 'post', 'created_at']
        extra_kwargs = {  
            'user':{'write_only':True},
            'post':{'write_only':True},
            'created_at':{'read_only':True},
        }


class CommentLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment', 'created_at']
        extra_kwargs = {  
            'user':{'write_only':True},
            'comment':{'write_only':True},
            'created_at':{'read_only':True},
            'id':{'read_only':True},
        }