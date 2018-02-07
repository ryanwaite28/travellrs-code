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



# --- GET Functions --- #



def welcome(request):
    # user_session.clear()
    if 'session_id' in user_session:
        return redirect('/home')

    return render_template('welcome.html')


def signup_get(request):
    if request.method == "GET":
        if 'session_id' in user_session:
            return redirect('/')

        return render_template('signup.html')


def signin_get(request):
    if request.method == "GET":
        if 'session_id' in user_session:
            return redirect('/')

        return render_template('signin.html')

def signout_get(request):
    if 'session_id' in user_session:
        you = db_session.query(Users).filter_by(id = user_session['user_id']).one()

        you.last_loggedout = func.now()
        db_session.add(you)
        db_session.commit()

    user_session.clear()
    return redirect('/')


def home(request):
    if 'session_id' not in user_session:
        return redirect('/')

    return render_template('home.html')


def check_session_get(request):
    if 'session_id' in user_session:
        you = db_session.query(Users).filter_by(id = user_session['user_id']).one()
        return jsonify(online = True, user = you.serialize)

    else:
        return jsonify(online = False)


def get_random_travels(request):
    travels = db_session.query(Travels).order_by(func.random()).limit(15).all()
    return jsonify(message = 'random travels', travels = [t.serialize for t in travels])




# --- POST Functions --- #



def signup_post(request):
    if request.method == "POST":
        try:
            data = json.loads(request.data)
            if not data:
                return jsonify( error = True, message = 'request body is empty, check headers/data' )

            username   = str(data['username'])
            email      = str(data['email'])
            password   = str(data['password']).encode()

            hashed     = bcrypt.hashpw(password, bcrypt.gensalt())

            check_username     = db_session.query(Users).filter_by(username = username).first()
            check_email        = db_session.query(Users).filter_by(email = email).first()

            if check_username:
                return jsonify(error = True, message = 'username is taken')

            if check_email:
                return jsonify(error = True, message = 'email is already in use')

            new_user   = Users(username = username, email = email, password = hashed)
            db_session.add(new_user)
            db_session.commit()

            session_id                     = uniqueValue()
            user_session['session_id']     = session_id
            user_session['user_id']        = new_user.id

            return jsonify(session_id = session_id, user = new_user.serialize, message = 'Signed Up!')

        except Exception as err:
            print(err)
            return jsonify(error = True, errorMessage = str(err), message = 'error signing up...')



# --- PUT Functions --- #



def signin_put(request):
    if request.method == "PUT":
        try:
            data = json.loads(request.data)
            if not data:
                return jsonify( error = True, message = 'request body is empty, check headers/data' )

            email      = str(data['email'])
            password   = str(data['password']).encode()

            user       = db_session.query(Users).filter_by(email = email).first()

            if not user:
                return jsonify(error = True, message = 'invalid credentials')

            if bcrypt.checkpw(password, user.password.encode()) == False:
                return jsonify(error = True, message = 'invalid credentials')

            session_id                     = uniqueValue()
            user_session['session_id']     = session_id
            user_session['user_id']        = user.id

            return jsonify(session_id = session_id, user = user.serialize, message = 'Signed In!')

        except Exception as err:
            print(err)
            return jsonify(error = True, errorMessage = str(err), message = 'error signing in...')

def signout_put(request):
    if 'session_id' in user_session:
        you = db_session.query(Users).filter_by(id = user_session['user_id']).one()

        you.last_loggedout = func.now()
        session.add(you)
        session.commit()

    user_session.clear()
    return jsonify(message = 'signed out', online = False)



# --- DELETE Functions --- #






# --- MISC Functions --- #
