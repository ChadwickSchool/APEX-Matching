import barnum
import random
from database_setup import Project, Base, Student, Pref
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import session as login_session
# from server.dao import (Address, Group, Person, PersonEmail, PersonPhone,
#                         User, Position, Privilege)
engine = create_engine('sqlite:///testing.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def create_preferences(student):
    session_numbers = [1, 2, 3, 4]
    random.shuffle(session_numbers)
    pref_number = 1
    for session_number in session_number:
        projects = session.query(Project).filter_by(session_number=session_number).all()
        random_project = random.choice(projects)
        pref = Pref(pref_number=pref_number, name=random_project.name, student=student)
        session.add(pref)
        pref_number++
    session.commit()
    
students = session.query(Student).all()

for student in students:
    create_preferences(student)