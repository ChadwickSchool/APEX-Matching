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
MIN_STUDS_PER_GROUP = 10
NUM_OF_PROJS = 25
SESSION_1_PROJECTS = []
SESSION_2_PROJECTS = []
SESSION_3_PROJECTS = []
SESSION_4_PROJECTS = []


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


def clear_all_students():
    '''Sets all student's matched to 0 (not matched)'''
    students = SESSION.query(Student).all()
    for stud in students:
        stud.matched = 0
        SESSION.add(stud)
        SESSION.commit()


def get_raw_score(project):
    """
    Return # of students that have marked the given project as a preference
    """
    project_name = project.name
    prefs = SESSION.query(Pref).filter_by(name=project_name).all()
    return len(prefs)


def get_popularity_score(project):
    """
    Return weighted ranking of students' preference for given project
    """
    project_name = project.name
    prefs = SESSION.query(Pref).filter_by(name=project_name)
    first_prefs = prefs.filter_by(pref_number=1).all()
    second_prefs = prefs.filter_by(pref_number=2).all()
    third_prefs = prefs.filter_by(pref_number=3).all()
    fourth_prefs = prefs.filter_by(pref_number=4).all()
    total_score = len(first_prefs) * 4 + len(second_prefs) * \
        3 + len(third_prefs) * 2 + len(fourth_prefs)
    return total_score


def raw_sort(session_num):
    """Return the names of projects in order of lowest raw score to highest"""
    projs = []
    projects = SESSION.query(Project)
    projects = projects.filter_by(session_number=session_num).all()
    for proj in projects:
        proj.raw_score = get_raw_score(proj)
        SESSION.add(proj)
        SESSION.commit()
    projects = SESSION.query(Project).all()
    projects.sort(key=lambda Project: Project.raw_score, reverse=False)
    for proj in projects:
        projs.append(proj.name)
    return projs


def pop_sort(session_num):
    """Return the names of projects in order of lowest pop score to highest"""
    projs = []
    projects = SESSION.query(Project)
    projects = projects.filter_by(session_number=session_num).all()
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


def get_underfilled_groups(session_num):
    """Return the names of projects with deficient students to fill"""
    projs = []
    projects = raw_sort(session_num)
    for proj in projects:
        project = SESSION.query(Project).filter_by(name=proj).one()
        if project.raw_score < MIN_STUDS_PER_GROUP:
            projs.append(project.name)
    return projs


def give_all_prefs(session_num):
    """Return project objects of projects with all their prefs assigned"""
    # An underfilled project is a project where the number of students that want
    # the project (raw score) is less than the minimum students per project
    underfilled_projs_names = get_underfilled_groups(session_num)
    for proj_name in underfilled_projs_names:
        project = SESSION.query(Project).filter_by(name=proj_name).one()
        prefs = SESSION.query(Pref).filter_by(name=proj_name).all()
        student_names = []
        for pref in prefs:
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if student.matched is False:
                student_names.append(student.name)
                student.matched = True
                SESSION.add(student)
                SESSION.commit()
        raw_score = get_raw_score(project)
        pop_score = get_popularity_score(project)
        project_obj = Project_class(
            proj_name, student_names, raw_score, pop_score)
        if session_num = 1:
            SESSION_1_PROJECTS.extend(project_obj)
        if session_num = 2:
            SESSION_2_PROJECTS.extend(project_obj)
        if session_num = 3:
            SESSION_3_PROJECTS.extend(project_obj)
        if session_num = 4:
            SESSION_4_PROJECTS.extend(project_obj)
    return "it worked"


def give_first_prefs(session_num):
    """
    Return the project objects of projects with just their first prefs assigned
    """
    proj_names = pop_sort(session_num)
    for proj_name in proj_names:
        project = SESSION.query(Project).filter_by(name=proj_name).one()
        prefs = SESSION.query(Pref).filter_by(name=proj_name)
        prefs = prefs.filter_by(pref_number=1).all()
        student_names = []
        i = 0
        for pref in prefs:
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if student.matched is False:
                if i < MAX_STUDS_PER_GROUP:
                    student_names.append(student.name)
                    student.matched = True
                    SESSION.add(student)
                    SESSION.commit()
                    i = i + 1
        raw_score = get_raw_score(project)
        pop_score = get_popularity_score(project)
        project_obj = Project_class(proj, student_names, raw_score, pop_score)
        if session_num = 1:
            SESSION_1_PROJECTS.extend(project_obj)
        if session_num = 2:
            SESSION_2_PROJECTS.extend(project_obj)
        if session_num = 3:
            SESSION_3_PROJECTS.extend(project_obj)
        if session_num = 4:
            SESSION_4_PROJECTS.extend(project_obj)
    return "it worked"


def give_second_prefs(session_num):
    """
    Return the project objects of projects with their second prefs assigned
    """
    if session_num is 1:
        for proj in SESSION_1_PROJECTS:
            prefs = SESSION.query(Pref).filter_by(pref_number=2).all()
            for pref in prefs:
                student = SESSION.query(Student).filter_by(
                    id=pref.student_id).one()
                if student.matched is False and pref.name is proj.proj_name and len(proj.students) < MAX_STUDS_PER_GROUP:
                    proj.students.extend(student.name)
                    student.matched = True
                    SESSION.add(student)
                    SESSION.commit()
    if session_num is 2:
        for proj in SESSION_2_PROJECTS:
            prefs = SESSION.query(Pref).filter_by(pref_number=2).all()
            for pref in prefs:
                student = SESSION.query(Student).filter_by(
                    id=pref.student_id).one()
                if student.matched is False and pref.name is proj.proj_name and len(proj.students) < MAX_STUDS_PER_GROUP:
                    proj.students.extend(student.name)
                    student.matched = True
                    SESSION.add(student)
                    SESSION.commit()
    if session_num is 3:
        for proj in SESSION_3_PROJECTS:
            prefs = SESSION.query(Pref).filter_by(pref_number=2).all()
            for pref in prefs:
                student = SESSION.query(Student).filter_by(
                    id=pref.student_id).one()
                if student.matched is False and pref.name is proj.proj_name and len(proj.students) < MAX_STUDS_PER_GROUP:
                    proj.students.extend(student.name)
                    student.matched = True
                    SESSION.add(student)
                    SESSION.commit()
    if session_num is 4:
        for proj in SESSION_4_PROJECTS:
            prefs = SESSION.query(Pref).filter_by(pref_number=2).all()
            for pref in prefs:
                student = SESSION.query(Student).filter_by(
                    id=pref.student_id).one()
                if student.matched is False and pref.name is proj.proj_name and len(proj.students) < MAX_STUDS_PER_GROUP:
                    proj.students.extend(student.name)
                    student.matched = True
                    SESSION.add(student)
                    SESSION.commit()
    return "it worked"


def give_third_prefs(session_num):
    """
    Return the project objects of projects with their third prefs assigned
    """
    if session_num is 1:
        for proj in SESSION_1_PROJECTS:
            prefs = SESSION.query(Pref).filter_by(pref_number=3).all()
            for pref in prefs:
                student = SESSION.query(Student).filter_by(
                    id=pref.student_id).one()
                if student.matched is False and pref.name is proj.proj_name and len(proj.students) < MAX_STUDS_PER_GROUP:
                    proj.students.extend(student.name)
                    student.matched = True
                    SESSION.add(student)
                    SESSION.commit()
    if session_num is 2:
        for proj in SESSION_2_PROJECTS:
            prefs = SESSION.query(Pref).filter_by(pref_number=3).all()
            for pref in prefs:
                student = SESSION.query(Student).filter_by(
                    id=pref.student_id).one()
                if student.matched is False and pref.name is proj.proj_name and len(proj.students) < MAX_STUDS_PER_GROUP:
                    proj.students.extend(student.name)
                    student.matched = True
                    SESSION.add(student)
                    SESSION.commit()
    if session_num is 3:
        for proj in SESSION_3_PROJECTS:
            prefs = SESSION.query(Pref).filter_by(pref_number=3).all()
            for pref in prefs:
                student = SESSION.query(Student).filter_by(
                    id=pref.student_id).one()
                if student.matched is False and pref.name is proj.proj_name and len(proj.students) < MAX_STUDS_PER_GROUP:
                    proj.students.extend(student.name)
                    student.matched = True
                    SESSION.add(student)
                    SESSION.commit()
    if session_num is 4:
        for proj in SESSION_4_PROJECTS:
            prefs = SESSION.query(Pref).filter_by(pref_number=3).all()
            for pref in prefs:
                student = SESSION.query(Student).filter_by(
                    id=pref.student_id).one()
                if student.matched is False and pref.name is proj.proj_name and len(proj.students) < MAX_STUDS_PER_GROUP:
                    proj.students.extend(student.name)
                    student.matched = True
                    SESSION.add(student)
                    SESSION.commit()
    return "it worked"


def give_fourth_prefs(session_num):
    """
    Return the project objects of projects with just their fourth prefs assigned
    """
    if session_num is 1:
        for proj in SESSION_1_PROJECTS:
            prefs = SESSION.query(Pref).filter_by(pref_number=4).all()
            for pref in prefs:
                student = SESSION.query(Student).filter_by(
                    id=pref.student_id).one()
                if student.matched is False and pref.name is proj.proj_name and len(proj.students) < MAX_STUDS_PER_GROUP:
                    proj.students.extend(student.name)
                    student.matched = True
                    SESSION.add(student)
                    SESSION.commit()
    if session_num is 2:
        for proj in SESSION_2_PROJECTS:
            prefs = SESSION.query(Pref).filter_by(pref_number=4).all()
            for pref in prefs:
                student = SESSION.query(Student).filter_by(
                    id=pref.student_id).one()
                if student.matched is False and pref.name is proj.proj_name and len(proj.students) < MAX_STUDS_PER_GROUP:
                    proj.students.extend(student.name)
                    student.matched = True
                    SESSION.add(student)
                    SESSION.commit()
    if session_num is 3:
        for proj in SESSION_3_PROJECTS:
            prefs = SESSION.query(Pref).filter_by(pref_number=4).all()
            for pref in prefs:
                student = SESSION.query(Student).filter_by(
                    id=pref.student_id).one()
                if student.matched is False and pref.name is proj.proj_name and len(proj.students) < MAX_STUDS_PER_GROUP:
                    proj.students.extend(student.name)
                    student.matched = True
                    SESSION.add(student)
                    SESSION.commit()
    if session_num is 4:
        for proj in SESSION_4_PROJECTS:
            prefs = SESSION.query(Pref).filter_by(pref_number=4).all()
            for pref in prefs:
                student = SESSION.query(Student).filter_by(
                    id=pref.student_id).one()
                if student.matched is False and pref.name is proj.proj_name and len(proj.students) < MAX_STUDS_PER_GROUP:
                    proj.students.extend(student.name)
                    student.matched = True
                    SESSION.add(student)
                    SESSION.commit()
    return "it worked"


def get_unmatched_students():
    """Return students that are unmatched in a project called Not Matched"""
    students = SESSION.query(Student).filter_by(matched=0).all()
    project_objs = []
    studs = []
    for student in students:
        print student.name
        studs.append(student.name)
    project_obj = Project_class('Not Matched', studs, 0, 0)
    project_objs.append(project_obj)
    return project_objs


def give_room_number(room_nums, session_num):
    """Add room numbers for each project in database"""
    n = 0
    if session_num is 1:
        for room in room_nums:
            if n < NUM_OF_PROJS:
                proj = SESSION.query(Project).filter_by(id=n)
                proj.room_number = room
                SESSION.add(proj)
                SESSION.commit()
                n = n + 1
    if session_num is 2:
        for room in room_nums:
            if n < NUM_OF_PROJS:
                proj = SESSION.query(Project).filter_by(id=n)
                proj.room_number = room
                SESSION.add(proj)
                SESSION.commit()
                n = n + 1
    if session_num is 3:
        for room in room_nums:
            if n < NUM_OF_PROJS:
                proj = SESSION.query(Project).filter_by(id=n)
                proj.room_number = room
                SESSION.add(proj)
                SESSION.commit()
                n = n + 1
    if session_num is 4:
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
