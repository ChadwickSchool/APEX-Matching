"""Python file for APEX group making algorithm"""
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, engine, Project, Student, Pref
from project_class import Project_class


APP = Flask(__name__)
ENGINE = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSESSION = sessionmaker(bind=engine)
SESSION = DBSESSION()

NUMBER_OF_PREFS = 4
MAX_STUDS_PER_GROUP = 20
NUM_OF_PROJS = 25
PROJECTS = []


@APP.route('/')
@APP.route('/groups/')
def show_projects():
    """Returns list of projects in webpage"""
    give_all_prefs()
    give_first_prefs()
    give_second_prefs()
    give_third_prefs()
    give_fourth_prefs()
    return render_template('main.html', projects=PROJECTS)


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
    third_prefs = prefs.filter_by(pref_number=3).all()
    fourth_prefs = prefs.filter_by(pref_number=4).all()
    total_score = len(first_prefs) * 4 + len(second_prefs) * \
        3 + len(third_prefs) * 2 + len(fourth_prefs)
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
        if project.raw_score < 10:
            projs.append(project.name)
    return projs


def give_all_prefs():
    """Return project objects of projects with all their prefs assigned"""
    projs = get_underfilled_groups()
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
        PROJECTS.extend(project_obj)
    return PROJECTS


def give_first_prefs():
    """
    Return the project objects of projects with just their first prefs assigned
    """
    projs = pop_sort()
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
        PROJECTS.extend(project_obj)
    return PROJECTS


def give_second_prefs():
    """
    Return the project objects of projects with their second prefs assigned
    """
    for proj in PROJECTS:
        prefs = SESSION.query(Pref).filter_by(matched=0)
        prefs = prefs.filter_by(pref_number=2).all()
        for pref in prefs:
            if pref.name is proj.proj_name:
                if len(proj.students) < MAX_STUDS_PER_GROUP:
                    student = SESSION.query(
                        Student).filter_by(id=pref.id).one()
                    proj.students.extend(student.first_name)
                    student.matched = 1
                    SESSION.add(student)
                    SESSION.commit()
    return PROJECTS


def give_third_prefs():
    """
    Return the project objects of projects with their third prefs assigned
    """
    for proj in PROJECTS:
        prefs = SESSION.query(Pref).filter_by(matched=0)
        prefs = prefs.filter_by(pref_number=3).all()
        for pref in prefs:
            if pref.name is proj.proj_name:
                if len(proj.students) < MAX_STUDS_PER_GROUP:
                    student = SESSION.query(
                        Student).filter_by(id=pref.id).one()
                    proj.students.extend(student.first_name)
                    student.matched = 1
                    SESSION.add(student)
                    SESSION.commit()
    return PROJECTS


def give_fourth_prefs():
    """
    Return the project objects of projects with just their fourth prefs assigned
    """
    for proj in PROJECTS:
        prefs = SESSION.query(Pref).filter_by(matched=0)
        prefs = prefs.filter_by(pref_number=4).all()
        for pref in prefs:
            if pref.name is proj.proj_name:
                if len(proj.students) < MAX_STUDS_PER_GROUP:
                    student = SESSION.query(
                        Student).filter_by(id=pref.id).one()
                    proj.students.extend(student.first_name)
                    student.matched = 1
                    SESSION.add(student)
                    SESSION.commit()
    return PROJECTS


def get_unmatched_students():
    """Return students that are unmatched in a project called Not Matched"""
    students = SESSION.query(Student).filter_by(matched=0).all()
    project_objs = []
    studs = []
    for student in students:
        print student.first_name
        studs.append(student.first_name)
    project_obj = Project_class('Not Matched', studs, 0, 0)
    project_objs.append(project_obj)
    return project_objs


def give_room_number(room_nums):
    """Add room numbers for each project in database"""
    n = 0
    for room in room_nums:
        if n < NUM_OF_PROJS:
            proj = SESSION.query(Project).filter_by(id=n)
            proj.room_number = room
            SESSION.add(proj)
            SESSION.commit()
            n = n + 1


if __name__ == '__main__':
    APP.secret_key = 'super_secret_key'
    APP.debug = True
    APP.run(host='0.0.0.0', port=5000)
