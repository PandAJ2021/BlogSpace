from rest_framework import serializers
from .models import Follow, Subscribe
from accounts.models import User


class FollowSerializer(serializers.ModelSerializer):
    author = serializers.SlugField('username')

    class Meta:
        model = Follow
        fields = ['id', 'author' , 'created_at']
        extra_kwargs = {
            'created_at':{'read_only':True},
            'id':{'read_only':True},
        }
            
    def validate(self, data):
        follower = self.context['request'].user

        username = data.pop('author', None)
        if not username:
            raise serializers.ValidationError({'author':'this field is required'})
        
        try:
            author = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'author':'User Not found'})

        if author == follower:
            raise serializers.ValidationError({'author':'You cannot follow yourself'})
        
        if Follow.objects.filter(author=author, follower=follower).exists():
            raise serializers.ValidationError({'author':f'You already follow {author}'})
        
        data['author'] = author
        data['follower'] = follower
        
        return data