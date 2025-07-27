from rest_framework import serializers
from .models import Follow, Subscribe
from accounts.models import User


class FollowSerializer(serializers.ModelSerializer):
    author = serializers.SlugField('username')

    class Meta:
        model = Follow
        fields = ['id', 'author' , 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        try:
            author = User.objects.get(username=data['author'])
        except User.DoesNotExist:
            raise serializers.ValidationError({'author':'User Not found'})
        
        follower = self.context['request'].user
        if author == follower:
            raise serializers.ValidationError({'author':'You cannot follow yourself'})
        
        if Follow.objects.filter(author=author, follower=follower).exists():
            raise serializers.ValidationError({'author':f'You already follow {author}'})
        
        data['author'] = author
        data['follower'] = follower
        return data


class SubscribeCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugField('username')
    duration = serializers.ChoiceField(choices=[(1, 'a month'),(3, 'three months'),(6, 'six months'),(12, 'a year')])

    class Meta:
        model = Subscribe
        fields = ['author', 'created_at', 'updated_at', 'duration', 'expired_at', 'is_active']
        read_only_fields = ['created_at', 'updated_at', 'expired_at', 'is_active']

    def validate(self, data):
        try:
            author = User.objects.get(username=data['author'])
        except User.DoesNotExist:
            raise serializers.ValidationError({'author':'User not found'})
        
        subscriber = self.context['request'].user
        if author == subscriber:
            raise serializers.ValidationError({'author':'You cannot subscribe yourself'})
        
        data['author'] = author
        data['subscriber'] = subscriber        
        return data
        
    def create(self, validated_data):
        existing  = Subscribe.objects.filter(author=validated_data['author'], subscriber=validated_data['subscriber']).first()
        if existing :
            if existing.is_active:
                raise serializers.ValidationError({'author':f'You already have active subscription until {existing.expired_at}'})
            else:
                raise serializers.ValidationError({'author':f'Your subscription expired at {existing.expired_at}, update by id #{existing.id}'})
        return super().create(validated_data)


class SubscribeUpdateSerializer(serializers.ModelSerializer):
    author = serializers.SlugField('username', read_only=True)
    duration = serializers.ChoiceField(choices=[(1, 'a month'),(3, 'three months'),(6, 'six months'),(12, 'a year')])

    class Meta:
        model = Subscribe
        fields = ['author', 'created_at', 'updated_at', 'duration', 'expired_at', 'is_active']
        read_only_fields = ['author', 'created_at', 'updated_at', 'expired_at', 'is_active']

    def update(self, instance, validated_data):
        if instance.is_active:
            raise serializers.ValidationError({'author':f'You already have active subscription until {instance.expired_at}'})
        return super().update(instance, validated_data)