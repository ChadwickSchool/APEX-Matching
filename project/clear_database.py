import random
from database_setup import Project, Base, Student, Pref, project_student_link
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import session as login_session
# from server.dao import (Address, Group, Person, PersonEmail, PersonPhone,
#                         User, Position, Privilege)
engine = create_engine('sqlite:///test.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

projects = session.query(Project).all()

for project in projects:
    project.raw_score = 0
    project.pop_score = 0
    session.add(project)
    

students = session.query(Student).all()
for student in students:
    student.session_1_matched = False
    student.session_2_matched = False
    student.session_3_matched = False
    student.session_4_matched = False
    session.add(student)
    

# session.query(project_student_link).delete()
session.commit()
    
