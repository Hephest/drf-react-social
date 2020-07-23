from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from . import utils
from .models import Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'owner',
            'created_at',
            'updated_at',
            'content',
            'is_fan',
            'total_likes',
        )

    def get_is_fan(self, obj):
        user = self.context.get('request').user
        return utils.is_fan(obj, user)


class FanSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
        )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=32,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password'
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        user.save()
        return user
