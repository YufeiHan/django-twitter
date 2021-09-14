from newsfeeds.models import NewsFeed
from friendships.services import FriendshipService


class NewsFeedService(object):
    @classmethod
    def fanout_to_followers(cls, tweet):
        # 正确的方法：使用 bulk_create，会把 insert 语句合成一条
        newsfeeds = [
            NewsFeed(user=follower, tweet=tweet)
            for follower in FriendshipService.get_followers(tweet.user)
        ]
        newsfeeds.append(NewsFeed(user=tweet.user, tweet=tweet))
        NewsFeed.objects.bulk_create(newsfeeds)