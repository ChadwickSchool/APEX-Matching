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
    if len(project.students) > 20:
        print project.name
        print len(project.students)
        print project.session_number