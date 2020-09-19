import os

from flask import Flask
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/survey')
    def survey():
        return render_template('survey.html')

    @app.route('/signup')
    def signup():
        return render_template('signup.html')

    @app.route('/bounties')
    def bounties():
        return render_template('bounties.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/addBounty')
    def add_bounty():
        return render_template('addBounty.html')

    @app.route('/bounty')
    def bounty():
        return render_template('bounty.html')

    return app