# --- Modules/Functions --- #

import os , sys , cgi , re, hmac, hashlib, smtplib, requests, datetime
import logging, dateutil, sqlite3, urllib, httplib2, json, psycopg2
import random, string, bcrypt

from functools import wraps
from datetime import timedelta
from threading import Timer
from dateutil import parser

from flask import Flask, make_response, g, request, send_from_directory
from flask import render_template, url_for, redirect, flash, jsonify
from flask import session as user_session
from werkzeug.utils import secure_filename

from sqlalchemy import cast, exc, select
from sqlalchemy import desc, or_
from sqlalchemy.sql import func
from sqlalchemy.exc import InvalidRequestError, ArgumentError, StatementError, OperationalError, InternalError
from jinja2.ext import do

import models
from models import Base, db_session
from models import Users, Follows, FollowRequests
from models import Travels, TravelLikes, TravelComments, CommentLikes
from models import Photos, Videos

import vault
from vault import uniqueValue

import brain



# --- Setup --- #

app = Flask(__name__)
app.secret_key = 'DF6Y#6G1$56F)$JD8*4G!?/Eoifht496dfgs3TYD5$)F&*DFj/Y4DR'

def login_required(f):
    ''' Checks If User Is Logged In '''
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'session_id' in user_session:
            return f(*args, **kwargs)
        else:
            flash('Please Log In To Use This Site.')
            return redirect('/login')

    return decorated_function
# ---



# --- GET Routes --- #



@app.route('/', methods=['GET'])
def welcome():
    return brain.welcome(request)


@app.route('/signup', methods=['GET'])
def signup_get():
    return brain.signup_get(request)


@app.route('/signin', methods=['GET'])
def signin_get():
    return brain.signin_get(request)


@app.route('/signout', methods=['GET'])
def signout_get():
    return brain.signout_get(request)


@app.route('/home', methods=['GET'])
def home():
    return brain.home(request)


@app.route('/check_session', methods=['GET'])
def check_session_get():
    return brain.check_session_get(request)


@app.route('/get/travels/random', methods=['GET'])
def get_random_travels():
    return brain.get_random_travels(request)



# --- POST Routes --- #



@app.route('/signup', methods=['POST'])
def signup_post():
    return brain.signup_post(request)



# --- PUT Routes --- #



@app.route('/signin', methods=['PUT'])
def signin_put():
    return brain.signin_put(request)


@app.route('/signout', methods=['PUT'])
def signout_put():
    return brain.signout_put(request)




# --- DELETE Routes --- #







# --- API Routes --- #







# --- Listen --- #

# print(db_session)
if __name__ == '__main__':
    app.debug = True
    app.run( host = '0.0.0.0' , port = 5000 )
