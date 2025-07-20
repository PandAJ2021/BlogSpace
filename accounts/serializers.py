from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
import re


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='Confirm Password', write_only=True)

    class Meta:
        model = User
        fields = ['phone', 'email', 'username', 'password', 'password2']
        extra_kwargs = {
            'email': {'validators':[UniqueValidator(User.objects.all())]},
            'username': {'validators':[UniqueValidator(User.objects.all())]},
            'password': {'write_only':True},
        }

    def validate_phone(self, value):
        if not re.fullmatch('09\d{9}', value):
            raise serializers.ValidationError('Enter a valid 11-dgigit phone number')
        return value
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords must match')
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)
    

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'email', 'username', 'password', 'is_active', 'is_admin']
        extra_kwargs = {
            'email': {'validators':[UniqueValidator(User.objects.all())]},
            'username': {'validators':[UniqueValidator(User.objects.all())]},
            'password':{'write_only':True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    def validate_phone(self, value):
        if not re.fullmatch('09\d{9}', value):
            raise serializers.ValidationError('Enter a valid 11-dgigit phone number')
        return value
