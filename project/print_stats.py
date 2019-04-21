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
session = DBSESSION()

def print_preference_stats():
    students = session.query(Student).all()
    first_prefs = 0
    second_prefs = 0
    third_prefs = 0
    fourth_prefs = 0
    for student in students:
        prefs = session.query(Pref).filter_by(student_id=student.id).all()
        for pref in prefs:
            project = session.query(Project).filter_by(name=pref.name).first()
            if project is None:
                print pref.name
                continue
            if student in project.students:
                if pref.pref_number == 1:
                    first_prefs += 1
                elif pref.pref_number == 2:
                    second_prefs += 1
                elif pref.pref_number == 3:
                    third_prefs += 1
                elif pref.pref_number == 4:
                    fourth_prefs += 1

    print "First Preferences: " + str(first_prefs)
    print "Second Preferences: " + str(second_prefs)
    print "Third Preferences: " + str(third_prefs)
    print "Fourth Preferences: " + str(fourth_prefs)

def print_not_matched_students():
    not_matched_1 = ['Kira Corbalis']
    not_matched_2 = []
    not_matched_3 = ['Elizabeth Garrett', 'Aleksa Jarasunas', 'Richard Fu', 'Morgan Amberg', 'Natalie Fox']
    not_matched_4 = ['Michael Huang']
    
    no_matches = [not_matched_1, not_matched_2, not_matched_3, not_matched_4]
    
    session_number = 1
    for no_match in no_matches:
        for name in no_match:
            student = session.query(Student).filter_by(name=name).first()
            preferences = session.query(Pref).filter_by(student_id=student.id).all()
            print student.name
            for pref in preferences:
                print str(pref.pref_number) + ': ' + pref.name


print_not_matched_students()