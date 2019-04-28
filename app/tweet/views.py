from flask import render_template, url_for, redirect, flash, abort
from flask_login import current_user
from .. import db
from ..models import User, Tweet
from . import tweet
from .forms import CommentForm
from ..queries import get_tweet, send_comment, get_comments

@tweet.route('/<tweet_id>', methods=['GET', 'POST'])
def tweetpage(tweet_id):
    t = get_tweet(tweet_id)
    commentform = CommentForm()
    if commentform.validate_on_submit():
        handle_comment_request(commentform.message.data, tweet_id)
        return redirect(url_for('tweet.tweetpage', tweet_id=tweet_id))
    if t is None:
        return abort(404)
    else:
        return render_template('tweet/tweet.html.j2',tweet=t, comments=get_comments(tweet_id), commentform=commentform)

# adds comment if the user is logged in
# String, Integer -> DB
def handle_comment_request(msg, tweet_id):
    if current_user.is_authenticated:
        send_comment(msg, current_user, tweet_id)
    else:
        flash("You must be signed in to comment!")
