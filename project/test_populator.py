"""Python file to populate database with fake data"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Student, engine, Pref, Project

ENGINE = create_engine('sqlite:///database.db')
Base.metadata.bind = ENGINE
DBSESSION = sessionmaker(bind=ENGINE)
SESSION = DBSESSION()

"""Create and add projects A-H to database"""
project_A = Project(name='A', session_number=1)
project_B = Project(name='B', session_number=1)
project_C = Project(name='C', session_number=2)
project_D = Project(name='D', session_number=2)
project_E = Project(name='E', session_number=3)
project_F = Project(name='F', session_number=3)
project_G = Project(name='G', session_number=4)
project_H = Project(name='H', session_number=4)

SESSION.add(project_A)
SESSION.add(project_B)
SESSION.add(project_C)
SESSION.add(project_D)
SESSION.add(project_E)
SESSION.add(project_F)
SESSION.add(project_G)
SESSION.add(project_H)

SESSION.commit()
