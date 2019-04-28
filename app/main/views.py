from flask import render_template, session, redirect, url_for, current_app, flash
from flask_login import current_user
from .. import db
from ..models import User
from . import main
from ..queries import get_all_tweets, toggle_like

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html.j2',
                           tweets=get_all_tweets(None, current_user))

@main.route('/like/<tweet_id>', methods=['GET', 'POST'])
def like(tweet_id):
    if current_user.is_authenticated:
        toggle_like(tweet_id, current_user)
    else:
        flash("You must be logged in to like!")
    return redirect(url_for('main.index'))
