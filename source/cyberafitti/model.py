# coding: utf-8
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Bj(db.Model):
    __tablename__ = 'Bj'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    blacklist = db.Column(db.Boolean, nullable=False, default=False)
    seen = db.Column(db.Boolean, nullable=False, default=False)
    per = db.Column(db.Integer, nullable=False, default=0)
    platform_id = db.Column(db.ForeignKey('Platform.id'), nullable=False)

    platform = db.relationship('Platform', primaryjoin='Bj.platform_id == Platform.id', backref='bjs')


class Platform(db.Model):
    __tablename__ = 'Platform'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
