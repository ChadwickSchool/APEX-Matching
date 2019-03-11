"""Python file for APEX group making algorithm"""
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, engine, Project, Student, Pref
from project_class import Project_class


APP = Flask(__name__)
ENGINE = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSESSION = sessionmaker(bind=engine)
SESSION = DBSESSION()

NUMBER_OF_PREFS = 2
MAX_STUDS_PER_GROUP = 5


def get_raw_score(project):
    """Return the raw score of given project"""
    project_name = project.name
    prefs = SESSION.query(Pref).filter_by(name=project_name).all()
    return len(prefs)


def get_popularity_score(project):
    """Return the popularity score of given project"""
    project_name = project.name
    prefs = SESSION.query(Pref).filter_by(name=project_name)
    first_prefs = prefs.filter_by(pref_number=1).all()
    second_prefs = prefs.filter_by(pref_number=2).all()
    total_score = len(first_prefs) * 2 + len(second_prefs)
    return total_score

def raw_sort():
    """Return the names of projects in order of lowest raw score to highest"""
    projs = []
    projects = SESSION.query(Project).all()
    for proj in projects:
        proj.raw_score = get_raw_score(proj)
        SESSION.add(proj)
        SESSION.commit()
    projects = SESSION.query(Project).all()
    projects.sort(key=lambda Project: Project.raw_score, reverse=False)
    for proj in projects:
        projs.append(proj.name)
    return projs


def pop_sort():
    """Return the names of projects in order of lowest pop score to highest"""
    projs = []
    projects = SESSION.query(Project).all()
    for proj in projects:
        proj.pop_score = get_popularity_score(proj)
        proj.raw_score = get_raw_score(proj)
        SESSION.add(proj)
        SESSION.commit()
    projects = SESSION.query(Project).all()
    projects.sort(key=lambda Project: Project.raw_score, reverse=False)
    for proj in projects:
        if proj.raw_score > 2:
            projs.append(proj.name)
    return projs


def get_underfilled_groups():
    """Return the names of projects with deficient students to fill"""
    projs = []
    projects = raw_sort()
    for proj in projects:
        project = SESSION.query(Project).filter_by(name=proj).one()
        if project.raw_score < 3:
            projs.append(project.name)
    return projs


def give_all_prefs():
    """Return project objects of projects with all their prefs assigned"""
    projs = get_underfilled_groups()
    project_objs = []
    for proj in projs:
        project = SESSION.query(Project).filter_by(name=proj).one()
        students = SESSION.query(Pref).filter_by(name=proj).all()
        student_names = []
        for stud in students:
            student = SESSION.query(Student).filter_by(
                id=stud.student_id).one()
            if student.matched is 0:
                student_names.append(student.first_name)
                student.matched = 1
                SESSION.add(student)
                SESSION.commit()
        raw_score = get_raw_score(project)
        pop_score = get_popularity_score(project)
        project_obj = Project_class(proj, student_names, raw_score, pop_score)
        project_objs.append(project_obj)
        print "project name: " + project_obj.proj_name
        print "students: "
        print project_obj.students
        print '\n'
    return project_objs


def give_first_prefs():
    """
    Return the project objects of projects with just their first prefs assigned
    """
    projs = pop_sort()
    project_objs = []
    for proj in projs:
        project = SESSION.query(Project).filter_by(name=proj).one()
        students = SESSION.query(Pref).filter_by(name=proj)
        students = students.filter_by(pref_number=1).all()
        student_names = []
        i = 0
        for stud in students:
            student = SESSION.query(Student).filter_by(
                id=stud.student_id).one()
            if student.matched is 0:
                if i < MAX_STUDS_PER_GROUP:
                    student_names.append(student.first_name)
                    student.matched = 1
                    SESSION.add(student)
                    SESSION.commit()
                    i = i + 1
        raw_score = get_raw_score(project)
        pop_score = get_popularity_score(project)
        project_obj = Project_class(proj, student_names, raw_score, pop_score)
        project_objs.append(project_obj)
        print "project name: " + project_obj.proj_name
        print "students: "
        print project_obj.students
        print '\n'
    return project_objs


def get_unmatched_students():
    """Return first names of students not assigned to a project"""
    students = SESSION.query(Student).filter_by(matched=0).all()
    studs = []
    for student in students:
        studs.append(student.first_name)
    print "Unmatched Students: "
    print studs
    return studs
