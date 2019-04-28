from .models import User, Tweet, Comment, TweetLike
from . import db

# adds a tweet to the DB
# String, User -> DB
def send_tweet(msg, user):
    tweet = Tweet(message=msg, user_id=user.id)
    db.session.add(tweet)
    db.session.commit()

# adds a tweet to the DB
# String, User, Int -> DB
def send_comment(msg, user, tweet_id):
    comment = Comment(message=msg, user_id=user.id, tweet_id=tweet_id)
    db.session.add(comment)
    db.session.commit()

# gets all of a user's tweets in a readable format,
# or returns all tweets if no user is provided
# User, User -> {User, Tweet}
def get_all_tweets(user_by = None, user_view = None):
    queryobj =  db.session.query(User, Tweet).join(Tweet)
    if user_by is not None:
        queryobj = queryobj.filter(User.id == user_by.id)
    return map(lambda q : {'user': q.User, 'tweet' : q.Tweet, 'no_likes' : get_no_likes(q.Tweet.tweet_id), 'user_liked' : has_liked(q.Tweet.tweet_id, user_view)}, queryobj.order_by(Tweet.timestamp.desc()).all()) #map(lambda q : [q.User.username, q.Tweet.message], queryobj

# gets a user by its username
# String -> User
def get_user(un):
    return User.query.filter_by(username=un).first()

# gets a tweet by id
# Integer -> Tweet
def get_tweet(t_id):
    queryobj =  db.session.query(User, Tweet).join(Tweet).filter(Tweet.tweet_id==t_id).first()
    return {'user': queryobj.User, 'tweet' : queryobj.Tweet, 'no_likes' : get_no_likes(queryobj.Tweet.tweet_id)}

# gets number of likes for a tweet
# Tweet_id -> Integer
def get_no_likes(tweet_id):
    return TweetLike.query.filter_by(tweet_id=tweet_id).count()

# checks if the given user has liked the tweet
# Tweet_id, User_id -> Boolean
def has_liked(tweet_id,user):
    return TweetLike.query.filter_by(tweet_id=tweet_id).filter_by(user_id=user.id).first() is not None

# gets a tweet's comments and the associated user
# Integer -> {User, Comment}
def get_comments(tweet_id):
    queryobj =  db.session.query(User, Comment).join(Comment).filter(Comment.tweet_id == tweet_id)
    return queryobj.order_by(Comment.timestamp.desc()).all() #map(lambda q : [q.User.username, q.Tweet.message], queryobj)

# toggles a like for a tweet by a user
# Tweet_id, User -> DB
def toggle_like(tweet_id, user):
    queryobj = db.session.query(TweetLike).filter(TweetLike.tweet_id == tweet_id).filter(TweetLike.user_id == user.id)
    if queryobj.first() is None:
        tweetlike = TweetLike(tweet_id=tweet_id, user_id=user.id)
        db.session.add(tweetlike)
        db.session.commit()
    else:
        db.session.delete(queryobj.first())
        db.session.commit()
