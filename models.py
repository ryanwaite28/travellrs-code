import sys, os, psycopg2, string, random

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from sqlalchemy.sql import func

from vault import uniqueValue



Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id                  = Column(Integer, primary_key = True)

    username            = Column(String(80), nullable = False)
    email               = Column(String(80), nullable = False)
    password            = Column(String(80), nullable = False)

    icon                = Column(String, default = '/static/img/anon.png')
    bio                 = Column(String(250), default = '')
    public              = Column(Boolean, nullable = False, default = True)

    date_created        = Column(DateTime, server_default=func.now())
    last_loggedin       = Column(DateTime, server_default=func.now())
    last_loggedout      = Column(DateTime)

    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,

            'username': self.username,
            'email': self.email,
            'icon': self.icon,
            'bio': self.bio,
            'public': self.public,

            'date_created': str(self.date_created),
            'last_loggedin': str(self.last_loggedin),
            'last_loggedout': str(self.last_loggedout),

            'unique_value': self.unique_value
        }
# ---

class Follows(Base):
    __tablename__ = 'follows'

    id                  = Column(Integer, primary_key = True)

    user_id             = Column(Integer, ForeignKey('users.id'))
    user_rel            = relationship('Users', foreign_keys=[user_id])

    follows_id          = Column(Integer, ForeignKey('users.id'))
    follows_rel         = relationship('Users', foreign_keys=[follows_id])

    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,

            'user_id': self.user_id,
            'user': self.user_rel.serialize,

            'follows_id': self.follows_id,
            'follows': self.follows_rel.serialize,

            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }
# ---

class FollowRequests(Base):
    __tablename__ = 'follow_requests'

    id                  = Column(Integer, primary_key = True)

    user_id             = Column(Integer, ForeignKey('users.id'))
    user_rel            = relationship('Users', foreign_keys=[user_id])

    requests_id         = Column(Integer, ForeignKey('users.id'))
    requests_rel        = relationship('Users', foreign_keys=[requests_id])

    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,

            'user_id': self.user_id,
            'user': self.user_rel.serialize,

            'requests_id': self.requests_id,
            'requests': self.requests_rel.serialize,

            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }
# ---

class Travels(Base):
    __tablename__ = 'travels'

    id                  = Column(Integer, nullable = False, primary_key = True)

    location            = Column(String, nullable = False)
    lat                 = Column(Float, nullable = False)
    lng                 = Column(Float, nullable = False)

    caption             = Column(String, nullable = False)
    icon                = Column(String, default = '/static/img/blank.png')
    place_id            = Column(String, nullable = False)

    owner_id            = Column(Integer, ForeignKey('users.id'))
    owner_rel           = relationship('Users')

    likes_rel           = relationship('TravelLikes', cascade='delete, delete-orphan', backref="TravelLikes")
    comments_rel        = relationship('TravelComments', cascade='delete, delete-orphan', backref="TravelComments")

    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,

            'location': self.location,
            'lat': self.lat,
            'lng': self.lng,

            'caption': self.caption,
            'icon': self.icon,
            'place_id': self.place_id,

            'owner_id': self.owner_id,
            'owner_rel': self.owner_rel.serialize,

            'likes': len(self.likes_rel),
            'comments': len(self.comments_rel),

            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }
# ---

class TravelLikes(Base):
    __tablename__ = 'travel_likes'

    id                  = Column(Integer, nullable = False, primary_key = True)

    travel_id           = Column(Integer, ForeignKey('travels.id'))
    travel_rel          = relationship('Travels')

    owner_id            = Column(Integer, ForeignKey('users.id'))
    owner_rel           = relationship('Users')

    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)


    @property
    def serialize(self):
        # Returns Data Object In Proper Format
        return {
            'id': self.id,

            'travel_id': self.travel_id,

            'owner_id': self.owner_id,
            'owner_rel': self.owner_rel.serialize,

            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }
# ---

class TravelComments(Base):
    __tablename__ = 'travel_comments'

    id                  = Column(Integer, nullable = False, primary_key = True)

    travel_id           = Column(Integer, ForeignKey('travels.id'))
    travel_rel          = relationship('Travels')

    owner_id            = Column(Integer, ForeignKey('users.id'))
    owner_rel           = relationship('Users')

    text                = Column(String, nullable = False)
    likes_rel           = relationship('CommentLikes', cascade='delete, delete-orphan', backref="CommentLikes")

    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)


    @property
    def serialize(self):
        # Returns Data Object In Proper Format
        return {
            'id': self.id,

            'travel_id': self.travel_id,

            'owner_id': self.owner_id,
            'owner_rel': self.owner_rel.serialize,

            'text': self.text,
            'likes': len(self.likes_rel),

            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }
# ---

class CommentLikes(Base):
    __tablename__ = 'comment_likes'

    id                  = Column(Integer, nullable = False, primary_key = True)

    comment_id          = Column(Integer, ForeignKey('travel_comments.id'))
    comment_rel         = relationship('TravelComments')

    owner_id            = Column(Integer, ForeignKey('users.id'))
    owner_rel           = relationship('Users')

    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)


    @property
    def serialize(self):
        # Returns Data Object In Proper Format
        return {
            'id': self.id,

            'comment_id': self.comment_id,

            'owner_id': self.owner_id,
            'owner_rel': self.owner_rel.serialize,

            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }
# ---

class Photos(Base):
    __tablename__ = 'photos'

    id                  = Column(Integer, nullable = False, primary_key = True)

    caption             = Column(String)
    link                = Column(String)

    owner_id            = Column(Integer, ForeignKey('users.id'))
    owner_rel           = relationship('Users')

    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
        # Returns Data Object In Proper Format
        return {
            'id': self.photo_id,

            'caption': self.caption,
            'link': self.link,

            'owner_id': self.owner_id,
            'owner_rel': self.owner_rel.serialize,

            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }
# ---

class Videos(Base):
    __tablename__ = 'videos'

    id                  = Column(Integer, nullable = False, primary_key = True)

    caption             = Column(String)
    link                = Column(String)

    owner_id            = Column(Integer, ForeignKey('users.id'))
    owner_rel           = relationship('Users')

    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
        # Returns Data Object In Proper Format
        return {
            'id': self.photo_id,

            'caption': self.caption,
            'link': self.link,

            'owner_id': self.owner_id,
            'owner_rel': self.owner_rel.serialize,

            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }
# ---





engine = create_engine('sqlite:///database.db', echo=True)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
db_session = DBSession()
