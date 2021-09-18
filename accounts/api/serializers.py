from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import exceptions

from accounts.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserSerializerWithProfile(UserSerializer):
    # user.profile 是我们在models里自定义的property
    # 通过 user.profile.nickname 来获取
    nickname = serializers.CharField(source='profile.nickname')
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'avatar_url')

    def get_avatar_url(self, obj):
        if obj.profile.avatar:
            return obj.profile.avatar.url
        return None


class UserSerializerForTweet(UserSerializerWithProfile):
    pass


class UserSerializerForFriendship(UserSerializerWithProfile):
    pass


class UserSerializerForComment(UserSerializerWithProfile):
    pass


class UserSerializerForLike(UserSerializerWithProfile):
    pass


# 检测request里有没有username和password这两项
class LoginSerializer(serializers.Serializer):
    # email = serializers.CharField(required=False)
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        data['username'] = data['username'].lower()
        if not User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'username': 'User does not exist.'
            })
        return data


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=6)
    password = serializers.CharField(max_length=20, min_length=6)
    email = serializers.EmailField()

    class Meta:
        model = User
        # 白名单模式，如果还有其他属性，是不会被添加的
        fields = ('username', 'email', 'password')

    # call is_valid() 的时候会被调用
    def validate(self, data):
        if User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'username': 'This username has been occupied.'
            })
        if User.objects.filter(email=data['email'].lower()).exists():
            raise exceptions.ValidationError({
                'email': 'This email address has been occupied.'
            })
        return data

    def create(self, validated_data):
        username = validated_data['username'].lower()
        email = validated_data['email'].lower()
        password = validated_data['password']

        # 通常是这么写 user = User.objects.create(username=username, ...)
        # 这里用django写好的，会帮你normalize username和Email，还会帮你加密password
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        # Create UserProfile object
        user.profile
        return user


class UserProfileSerializerForUpdate(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('nickname', 'avatar')
