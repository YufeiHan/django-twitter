from rest_framework import serializers

from accounts.api.serializers import UserSerializerForTweet
from comments.api.serializers import CommentSerializer
from tweets.models import Tweet


# ModelSerializer只需要在class Meta里指定field是什么，它就默认包含了，
# 不需要写content=serializers.CharField()之类的
class TweetSerializer(serializers.ModelSerializer):
    # 深入展开User里面是什么，没这行的话，User只会序列化为一个整数
    # 每一个field还可以是另外一个serializer
    user = UserSerializerForTweet()

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content')


class TweetSerializerForCreat(serializers.ModelSerializer):
    content = serializers.CharField(min_length=6, max_length=140)

    class Meta:
        model = Tweet
        fields = ('content',)  # 规定了只有content field可以写进去

    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content=content)
        return tweet


class TweetSerializerWithComments(TweetSerializer):
    comments = CommentSerializer(source='comment_set', many=True)

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'comments', 'created_at', 'content')

