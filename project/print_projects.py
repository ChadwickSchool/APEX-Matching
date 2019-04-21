"""Python file to populate database with project data from 2019"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Student, engine, Pref, Project

# ENGINE = create_engine('mysql+pymysql://chadwick:godolphins@apex-matching.c0plu8oomro4.us-east-2.rds.amazonaws.com:3306/testdb')
ENGINE = create_engine('sqlite:///test.db')
# ENGINE = create_engine('mysql+pymysql://chadwick:godolphins@apex-matching2.c0plu8oomro4.us-east-2.rds.amazonaws.com:3306/production')

# ENGINE = create_engine('mysql+pymysql://chadwick:godolphins@apex-matching16.c0plu8oomro4.us-east-2.rds.amazonaws.com:3306/production')


Base.metadata.bind = ENGINE
DBSESSION = sessionmaker(bind=ENGINE)
SESSION = DBSESSION()

# def add_proj_obj_to_database():
#     for project_object in SESSION.query(Project).filter_by(session_number=1):
#         print project_object.name
#         if project_object.name != 'Session 1 Not Matched':
#             project = SESSION.query(Project).filter_by(
#                 name=project_object.name).one()
#             for stud in project_object.students:
#                 student = SESSION.query(Student).filter_by(id=stud.id).one()
#                 project.students.append(student)
#                 SESSION.add(project)
#     for project_object in SESSION.query(Project).filter_by(session_number=2):
#         print project_object.name
#         if project_object.name != 'Session 2 Not Matched':
#             project = SESSION.query(Project).filter_by(
#                 name=project_object.name).one()
#             for stud in project_object.students:
#                 student = SESSION.query(Student).filter_by(id=stud.id).one()
#                 project.students.append(student)
#                 SESSION.add(project)
#     for project_object in SESSION.query(Project).filter_by(session_number=3):
#         print project_object.name
#         if project_object.name != 'Session 3 Not Matched':
#             project = SESSION.query(Project).filter_by(
#                 name=project_object.name).one()
#             for stud in project_object.students:
#                 student = SESSION.query(Student).filter_by(id=stud.id).one()
#                 project.students.append(student)
#                 SESSION.add(project)
#     for project_object in SESSION.query(Project).filter_by(session_number=4):
#         print project_object.name
#         if project_object.name != 'Session 4 Not Matched':
#             project = SESSION.query(Project).filter_by(
#                 name=project_object.name).one()
#             for stud in project_object.students:
#                 student = SESSION.query(Student).filter_by(id=stud.id).one()
#                 project.students.append(student)
#                 SESSION.add(project)
#     SESSION.commit()

# add_proj_obj_to_database()
for i in range(1, 5):
    print "Session: " + str(i)
    projects = SESSION.query(Project).filter_by(session_number=i).all()

    for project in projects:
        print project.name
        for student in project.students:
            print student.name

