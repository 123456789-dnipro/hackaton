from sqlalchemy import Column, Table
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, ARRAY, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

metadata = MetaData()

Base = declarative_base()

users = Table('users', metadata,
              Column('user_id', UUID, primary_key=True),
              Column('user_name', VARCHAR),
              Column('password', VARCHAR))

rooms = Table('rooms', metadata,
              Column('room_id', UUID, primary_key=True),
              Column('room_name', VARCHAR),
              Column('creator_id', UUID),
              Column('created_at', TIMESTAMP),
              Column('users', ARRAY(UUID)))

models = [users, rooms]
