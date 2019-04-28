from flask import Blueprint

tweet = Blueprint('tweet', __name__)

from . import views
