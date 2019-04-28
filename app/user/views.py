from flask import render_template, url_for, redirect, flash
from flask_login import current_user
from .. import db
from ..models import User, Tweet
from . import user
from .forms import TweetForm
from ..queries import get_all_tweets, send_tweet, get_user

@user.route('/<username>', methods=['GET', 'POST'])
def user(username):
    tweetform = TweetForm()
    u = get_user(username)
    if u is None:
        return abort(404)
    elif u == current_user:
        if tweetform.validate_on_submit():
            send_tweet(tweetform.message.data, u)
            return redirect(url_for('user.user', username = u.username))
        return render_template('user/myprofile.html.j2',user=u,tweets=get_all_tweets(u), tweetform=tweetform)
    else:
        return render_template('user/profile.html.j2',user=u, tweets=get_all_tweets(u))
