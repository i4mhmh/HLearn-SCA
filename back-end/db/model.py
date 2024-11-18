# -*- coding: utf-8 -*-
"""
"* Author     : M0nk3y"
"* Version    : 1.0"
"""

from sqlalchemy import Column, INTEGER, String
from .db import Base

class User(Base):
    __tablename__ = 'user'
    userid = Column(INTEGER, primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True)
    passwd = Column(String(255), nullable=False)
    fullname = Column(String(255), nullable=False)

    def __init__(self, username, passwd, fullname):
        self.username = username
        self.passwd = passwd
        self.fullname = fullname
