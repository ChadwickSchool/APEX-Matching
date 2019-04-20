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

# num_delete= session.query(Pref).filter_by(student_id=99).delete()
# print num_delete
# print session.query(Student).filter_by(email='jddevaughnbrown@chadwickschool.org').delete()
students = session.query(Student).all()
for student in students:
    student.session_1_matched = False
    student.session_2_matched = False
    student.session_3_matched = False
    student.session_4_matched = False
    session.add(student)

projects = session.query(Project).all()

for project in projects:
    project.raw_score = 0
    project.pop_score = 0
    session.add(project)
    

# for student in students:
#     print student.name
# session.query(Project).delete()

# F = Project(name='Take a Risk: An Antidote to an Overly Serious Youth: Bryce Baldridge', session_number=2)
# G = Project(name='We\'re Human, Too: Combatting Anti-Semitism in the Los Angeles Area: Sam Bogen', session_number=1)
# 
# session.add(F)
# session.add(G)

session.commit()
