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
    for session_number in session_numbers:
        projects = session.query(Project).filter_by(session_number=session_number).all()
        random_project = random.choice(projects)
        pref = Pref(pref_number=pref_number, name=random_project.name, student=student)
        session.add(pref)
        pref_number += 1
    session.commit()


def create_students():
    for i in range(0, 300):
        first_name, last_name = barnum.create_name()
        email = barnum.create_email(name=(first_name, last_name))
        student = Student(name=first_name + ' ' + last_name, email=email)
        session.add(student)
    session.commit()

create_students()
students = session.query(Student).all()

for student in students:
    create_preferences(student)
