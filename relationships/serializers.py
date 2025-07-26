from rest_framework import serializers
from models import Follow, Subscribe


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ['author', 'follower', 'created_at']
        extra_kwargs = {
            'created_at':{'read_only':True},
        }
            
    def validate(self, data):
        author = data['author']
        follower = data['follower']

        if author == follower:
            raise serializers.ValidationError('You cannot follow yourself')
        
        if Follow.objects.filter(author=author, follower=follower).exists():
            raise serializers.ValidationError(f'You already follow {author}')
        
        return data