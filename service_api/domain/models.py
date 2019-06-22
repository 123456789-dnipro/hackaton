from sqlalchemy import Column, Table
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, ARRAY, TIMESTAMP, INTEGER, BOOLEAN, BYTEA
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

metadata = MetaData()

Base = declarative_base()

users = Table('users', metadata,
              Column('user_id', UUID, primary_key=True, unique=True),
              Column('user_email', VARCHAR),
              Column('user_phone', VARCHAR, unique=True),
              Column('user_name', VARCHAR),
              Column('comfirmed', BOOLEAN),
              Column('comfirm_code', BOOLEAN))

photos = Table('files', metadata,
               Column('image_id', UUID, primary_key=True, unique=True),
               Column('image_name', UUID),
               Column('image_data', BYTEA),
               Column('passport_data', BYTEA),
               Column('user_id', UUID))

vehicles = Table('vehicle', metadata,
                 Column('plate', VARCHAR, primary_key=True, unique=True),
                 Column('owner_id', UUID),
                 Column('car_id', UUID, primary_key=True))

incedents = Table('incedents', metadata,
                  Column('incedent_id', UUID, primary_key=True, unique=True),
                  Column('created_at', TIMESTAMP),
                  Column('created_by', UUID),
                  Column('logituide', INTEGER),
                  Column('latitude', INTEGER))

incedents_points = Table('incedents_points', metadata,
                         Column('incedent_point_id', UUID, primary_key=True, unique=True))

models = [users, photos, vehicles, incedents, incedents_points]
