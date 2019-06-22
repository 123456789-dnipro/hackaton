from sqlalchemy import Column, Table
from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, TIMESTAMP, INTEGER, BOOLEAN, BYTEA

metadata = MetaData()

users = Table('users', metadata,
              Column('id', UUID, primary_key=True, unique=True),
              Column('phone', VARCHAR, unique=True))

files = Table('files', metadata,
               Column('id', UUID, primary_key=True, unique=True),
               Column('name', UUID),
               Column('data', BYTEA),
               Column('passport_data', BYTEA),
               Column('user_id', UUID))

vehicles = Table('vehicle', metadata,
                 Column('plate', VARCHAR, primary_key=True, unique=True),
                 Column('owner_id', UUID),
                 Column('car_id', UUID, primary_key=True),
                 Column('number', VARCHAR))

incedents = Table('incedents', metadata,
                  Column('id', UUID, primary_key=True, unique=True),
                  Column('created_at', TIMESTAMP),
                  Column('created_by', UUID),
                  Column('logituide', INTEGER), # TODO rename
                  Column('latitude', INTEGER))

incedents_points = Table('incedents_points', metadata,
                         Column('id', UUID, primary_key=True, unique=True))

models = [users, files, vehicles, incedents, incedents_points]
