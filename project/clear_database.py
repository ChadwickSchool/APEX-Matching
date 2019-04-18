"""Python file to populate database with fake data"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Student, engine, Pref, Project

# ENGINE = create_engine('mysql+pymysql://chadwick:godolphins@apex-matching.c0plu8oomro4.us-east-2.rds.amazonaws.com:3306/testdb')
# ENGINE = create_engine('mysql+pymysql://chadwick:godolphins@apex-matching2.c0plu8oomro4.us-east-2.rds.amazonaws.com:3306/production')
ENGINE = create_engine('sqlite:///database.db')
Base.metadata.bind = ENGINE
DBSESSION = sessionmaker(bind=ENGINE)
session = DBSESSION()

num_delete= session.query(Pref).delete()
print num_delete
print session.query(Student).delete()
# session.query(Project).delete()

session.commit()
