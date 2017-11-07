#-*- coding:utf-8 -*-

from flask import Flask, session, logging
from uuid import uuid4
import pickle
from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from database import db_session

class SQLAlchemySession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False

class SQLAlchemySessionInterface(SessionInterface):
    session_class = SQLAlchemySession
    serializer = pickle

    def generate_sid(self):
        return str(uuid4())

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)

        rec = db_session.query
