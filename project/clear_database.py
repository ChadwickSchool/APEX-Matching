"""Python file to populate database with fake data"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Student, engine, Pref, Project

# ENGINE = create_engine('mysql+pymysql://chadwick:godolphins@apex-matching.c0plu8oomro4.us-east-2.rds.amazonaws.com:3306/testdb')
# ENGINE = create_engine('mysql+pymysql://chadwick:godolphins@apex-matching2.c0plu8oomro4.us-east-2.rds.amazonaws.com:3306/production')
# ENGINE = create_engine('sqlite:///database.db')

ENGINE = create_engine('mysql+pymysql://chadwick:godolphins@apex-matching16.c0plu8oomro4.us-east-2.rds.amazonaws.com:3306/production')

Base.metadata.bind = ENGINE
DBSESSION = sessionmaker(bind=ENGINE)
session = DBSESSION()

# num_delete= session.query(Pref).delete()
# print num_delete
# print session.query(Student).filter_by(email='lsaltzmann2022@chadwickschool.org').delete()
# session.query(Project).delete()

F = Project(name='Our Mighty Mascot, the Bottlenose Dolphin: The Flaws in our Recycling Habits: Macy Dimson', session_number=1)
G = Project(name='We\'re Human, Too: Combatting Anti-Semitism in the Los Angeles Area: Sam Bogen', session_number=1)

session.add(F)
session.add(G)

session.commit()
