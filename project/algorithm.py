"""Python file for APEX group making algorithm"""
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, engine, Project, Student, Pref
from project_class import Project_class


APP = Flask(__name__)
ENGINE = create_engine('sqlite:///testing.db')
Base.metadata.bind = engine
DBSESSION = sessionmaker(bind=engine)
SESSION = DBSESSION()

NUMBER_OF_PREFS = 4
MAX_STUDS_PER_GROUP = 15
MIN_STUDS_PER_GROUP = 7
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


def get_raw_score(project):
    """
    Return # of students that have marked the given project as a preference
    """
    project_name = project.name
    prefs = SESSION.query(Pref).filter_by(name=project_name).all()
    return len(prefs)

# def sort_session_groups_by_number():
#     '''
#     makes lists of projects in order of how many students are in that group
#     '''
#


def add_proj_obj_to_database():
    for project_object in SESSION_1_PROJECTS:
        print project_object.proj_name
        if project_object.proj_name != 'Session 1 Not Matched':
            project = SESSION.query(Project).filter_by(
                name=project_object.proj_name).one()
            for stud in project_object.students:
                student = SESSION.query(Student).filter_by(name=stud).one()
                project.students.append(student)
                SESSION.add(project)
    for project_object in SESSION_2_PROJECTS:
        print project_object.proj_name
        if project_object.proj_name != 'Session 2 Not Matched':
            project = SESSION.query(Project).filter_by(
                name=project_object.proj_name).one()
            for stud in project_object.students:
                student = SESSION.query(Student).filter_by(name=stud).one()
                project.students.append(student)
                SESSION.add(project)
    for project_object in SESSION_3_PROJECTS:
        print project_object.proj_name
        if project_object.proj_name != 'Session 3 Not Matched':
            project = SESSION.query(Project).filter_by(
                name=project_object.proj_name).one()
            for stud in project_object.students:
                student = SESSION.query(Student).filter_by(name=stud).one()
                project.students.append(student)
                SESSION.add(project)
    for project_object in SESSION_4_PROJECTS:
        print project_object.proj_name
        if project_object.proj_name != 'Session 4 Not Matched':
            project = SESSION.query(Project).filter_by(
                name=project_object.proj_name).one()
            for stud in project_object.students:
                student = SESSION.query(Student).filter_by(name=stud).one()
                project.students.append(student)
                SESSION.add(project)
    SESSION.commit()


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


def raw_sort():
    """Return the names of projects in order of lowest raw score to highest"""
    projs = []
    projects = SESSION.query(Project)
    # projects = projects.filter_by(session_number=session_num).all()
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
    projects = SESSION.query(Project)
    # projects = projects.filter_by(session_number=session_num).all()
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
        if project.raw_score < MIN_STUDS_PER_GROUP:
            projs.append(project.name)
    return projs


def print_projects():
    '''prints all projects in each sesison'''
    print 'Session 1 Projects: '
    for proj in SESSION_1_PROJECTS:
        print 'Project: ' + proj.proj_name
        print 'Students: '
        print proj.students
    print 'Session 2 Projects: '
    for proj in SESSION_2_PROJECTS:
        print 'Project: ' + proj.proj_name
        print 'Students: '
        print proj.students
    print 'Session 3 Projects: '
    for proj in SESSION_3_PROJECTS:
        print 'Project: ' + proj.proj_name
        print 'Students: '
        print proj.students
    print 'Session 4 Projects: '
    for proj in SESSION_4_PROJECTS:
        print 'Project: ' + proj.proj_name
        print 'Students: '
        print proj.students


def give_all_prefs():
    """Return project objects of projects with all their prefs assigned"""
    # An underfilled project is a project where the number of students that want
    # the project (raw score) is less than the minimum students per project
    underfilled_projs_names = get_underfilled_groups()
    for project_name in underfilled_projs_names:
        project = SESSION.query(Project).filter_by(name=project_name).one()
        session_num = project.session_number
        prefs = SESSION.query(Pref).filter_by(name=project_name).all()
        student_names = []
        for pref in prefs:
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if session_num == 1:
                if student.session_1_matched is False:
                    student_names.append(student.name)
                    student.session_1_matched = True
                    SESSION.add(student)
                    SESSION.commit()
            if session_num == 2:
                if student.session_2_matched is False:
                    student_names.append(student.name)
                    student.session_2_matched = True
                    SESSION.add(student)
                    SESSION.commit()
            if session_num == 3:
                if student.session_3_matched is False:
                    student_names.append(student.name)
                    student.session_3_matched = True
                    SESSION.add(student)
                    SESSION.commit()
            if session_num == 4:
                if student.session_4_matched is False:
                    student_names.append(student.name)
                    student.session_4_matched = True
                    SESSION.add(student)
                    SESSION.commit()
        raw_score = get_raw_score(project)
        pop_score = get_popularity_score(project)
        project_obj = Project_class(
            project_name, student_names, raw_score, pop_score)
        if session_num == 1:
            SESSION_1_PROJECTS.append(project_obj)
        if session_num == 2:
            SESSION_2_PROJECTS.append(project_obj)
        if session_num == 3:
            SESSION_3_PROJECTS.append(project_obj)
        if session_num == 4:
            SESSION_4_PROJECTS.append(project_obj)
    return "it worked"


def give_first_prefs():
    """
    Return the project objects of projects with just their first prefs assigned
    """
    proj_names = pop_sort()
    for project_name in proj_names:
        project = SESSION.query(Project).filter_by(name=project_name).one()
        session_num = project.session_number
        prefs = SESSION.query(Pref).filter_by(name=project_name)
        prefs = prefs.filter_by(pref_number=1).all()
        student_names = []
        studs_in_proj = 0
        for pref in prefs:
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if session_num == 1:
                if student.session_1_matched is False:
                    if studs_in_proj < MAX_STUDS_PER_GROUP:
                        student_names.append(student.name)
                        student.session_1_matched = True
                        SESSION.add(student)
                        SESSION.commit()
                        studs_in_proj = studs_in_proj + 1
            if session_num == 2:
                if student.session_2_matched is False:
                    if studs_in_proj < MAX_STUDS_PER_GROUP:
                        student_names.append(student.name)
                        student.session_2_matched = True
                        SESSION.add(student)
                        SESSION.commit()
                        studs_in_proj = studs_in_proj + 1
            if session_num == 3:
                if student.session_3_matched is False:
                    if studs_in_proj < MAX_STUDS_PER_GROUP:
                        student_names.append(student.name)
                        student.session_3_matched = True
                        SESSION.add(student)
                        SESSION.commit()
                        studs_in_proj = studs_in_proj + 1
            if session_num == 4:
                if student.session_4_matched is False:
                    if studs_in_proj < MAX_STUDS_PER_GROUP:
                        student_names.append(student.name)
                        student.session_4_matched = True
                        SESSION.add(student)
                        SESSION.commit()
                        studs_in_proj = studs_in_proj + 1
        raw_score = get_raw_score(project)
        pop_score = get_popularity_score(project)
        project_obj = Project_class(
            project_name, student_names, raw_score, pop_score)
        if session_num == 1:
            SESSION_1_PROJECTS.append(project_obj)
        if session_num == 2:
            SESSION_2_PROJECTS.append(project_obj)
        if session_num == 3:
            SESSION_3_PROJECTS.append(project_obj)
        if session_num == 4:
            SESSION_4_PROJECTS.append(project_obj)
    return "it worked"


def give_second_prefs():
    """
    Return the project objects of projects with their second prefs assigned
    """
    SESSION_1_PROJECTS.sort(
        key=lambda Project: Project.num_studs, reverse=False)
    for proj in SESSION_1_PROJECTS:
        project_name = proj.proj_name
        project = SESSION.query(Project).filter_by(name=project_name).one()
        session_num = project.session_number
        prefs = SESSION.query(Pref).filter_by(name=project_name)
        prefs = prefs.filter_by(pref_number=2).all()
        student_names = []
        for pref in prefs:
            studs_in_proj = proj.num_studs
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if student.session_1_matched is False:
                if studs_in_proj < MAX_STUDS_PER_GROUP:
                    student_names.append(student.name)
                    student.session_1_matched = True
                    SESSION.add(student)
                    SESSION.commit()
                    if len(proj.students) is 0:
                        proj.students.append(student.name)
                    else:
                        proj.students.append(student.name)

    SESSION_2_PROJECTS.sort(
        key=lambda Project: Project.num_studs, reverse=False)
    for proj in SESSION_2_PROJECTS:
        project_name = proj.proj_name
        project = SESSION.query(Project).filter_by(name=project_name).one()
        session_num = project.session_number
        prefs = SESSION.query(Pref).filter_by(name=project_name)
        prefs = prefs.filter_by(pref_number=2).all()
        student_names = []
        for pref in prefs:
            studs_in_proj = proj.num_studs
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if student.session_2_matched is False:
                if studs_in_proj < MAX_STUDS_PER_GROUP:
                    student_names.append(student.name)
                    student.session_2_matched = True
                    SESSION.add(student)
                    SESSION.commit()
                    if len(proj.students) is 0:
                        proj.students.append(student.name)
                    else:
                        proj.students.append(student.name)

    SESSION_3_PROJECTS.sort(
        key=lambda Project: Project.num_studs, reverse=False)
    for proj in SESSION_3_PROJECTS:
        project_name = proj.proj_name
        project = SESSION.query(Project).filter_by(name=project_name).one()
        session_num = project.session_number
        prefs = SESSION.query(Pref).filter_by(name=project_name)
        prefs = prefs.filter_by(pref_number=2).all()
        student_names = []
        for pref in prefs:
            studs_in_proj = proj.num_studs
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if student.session_3_matched is False:
                if studs_in_proj < MAX_STUDS_PER_GROUP:
                    student_names.append(student.name)
                    student.session_3_matched = True
                    SESSION.add(student)
                    SESSION.commit()
                    if len(proj.students) is 0:
                        proj.students.append(student.name)
                    else:
                        proj.students.append(student.name)

    SESSION_4_PROJECTS.sort(
        key=lambda Project: Project.num_studs, reverse=False)
    for proj in SESSION_4_PROJECTS:
        project_name = proj.proj_name
        project = SESSION.query(Project).filter_by(name=project_name).one()
        session_num = project.session_number
        prefs = SESSION.query(Pref).filter_by(name=project_name)
        prefs = prefs.filter_by(pref_number=2).all()
        student_names = []
        for pref in prefs:
            studs_in_proj = proj.num_studs
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if student.session_4_matched is False:
                if studs_in_proj < MAX_STUDS_PER_GROUP:
                    student_names.append(student.name)
                    student.session_4_matched = True
                    SESSION.add(student)
                    SESSION.commit()
                    if len(proj.students) is 0:
                        proj.students.append(student.name)
                    else:
                        proj.students.append(student.name)


def give_third_prefs():
    """
    Return the project objects of projects with their second prefs assigned
    """
    SESSION_1_PROJECTS.sort(
        key=lambda Project: Project.num_studs, reverse=False)
    for proj in SESSION_1_PROJECTS:
        project_name = proj.proj_name
        project = SESSION.query(Project).filter_by(name=project_name).one()
        session_num = project.session_number
        prefs = SESSION.query(Pref).filter_by(name=project_name)
        prefs = prefs.filter_by(pref_number=3).all()
        student_names = []
        for pref in prefs:
            studs_in_proj = proj.num_studs
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if student.session_1_matched is False:
                if studs_in_proj < MAX_STUDS_PER_GROUP:
                    student_names.append(student.name)
                    student.session_1_matched = True
                    SESSION.add(student)
                    SESSION.commit()
                    if len(proj.students) is 0:
                        proj.students.append(student.name)
                    else:
                        proj.students.append(student.name)

    SESSION_2_PROJECTS.sort(
        key=lambda Project: Project.num_studs, reverse=False)
    for proj in SESSION_2_PROJECTS:
        project_name = proj.proj_name
        project = SESSION.query(Project).filter_by(name=project_name).one()
        session_num = project.session_number
        prefs = SESSION.query(Pref).filter_by(name=project_name)
        prefs = prefs.filter_by(pref_number=3).all()
        student_names = []
        for pref in prefs:
            studs_in_proj = proj.num_studs
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if student.session_2_matched is False:
                if studs_in_proj < MAX_STUDS_PER_GROUP:
                    student_names.append(student.name)
                    student.session_2_matched = True
                    SESSION.add(student)
                    SESSION.commit()
                    if len(proj.students) is 0:
                        proj.students.append(student.name)
                    else:
                        proj.students.append(student.name)

    SESSION_3_PROJECTS.sort(
        key=lambda Project: Project.num_studs, reverse=False)
    for proj in SESSION_3_PROJECTS:
        project_name = proj.proj_name
        project = SESSION.query(Project).filter_by(name=project_name).one()
        session_num = project.session_number
        prefs = SESSION.query(Pref).filter_by(name=project_name)
        prefs = prefs.filter_by(pref_number=3).all()
        student_names = []
        for pref in prefs:
            studs_in_proj = proj.num_studs
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if student.session_3_matched is False:
                if studs_in_proj < MAX_STUDS_PER_GROUP:
                    student_names.append(student.name)
                    student.session_3_matched = True
                    SESSION.add(student)
                    SESSION.commit()
                    if len(proj.students) is 0:
                        proj.students.append(student.name)
                    else:
                        proj.students.append(student.name)

    SESSION_4_PROJECTS.sort(
        key=lambda Project: Project.num_studs, reverse=False)
    for proj in SESSION_4_PROJECTS:
        project_name = proj.proj_name
        project = SESSION.query(Project).filter_by(name=project_name).one()
        session_num = project.session_number
        prefs = SESSION.query(Pref).filter_by(name=project_name)
        prefs = prefs.filter_by(pref_number=3).all()
        student_names = []
        for pref in prefs:
            studs_in_proj = proj.num_studs
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if student.session_4_matched is False:
                if studs_in_proj < MAX_STUDS_PER_GROUP:
                    student_names.append(student.name)
                    student.session_4_matched = True
                    SESSION.add(student)
                    SESSION.commit()
                    if len(proj.students) is 0:
                        proj.students.append(student.name)
                    else:
                        proj.students.append(student.name)


def give_fourth_prefs():
    """
    Return the project objects of projects with their fourth prefs assigned
    """
    SESSION_1_PROJECTS.sort(
        key=lambda Project: Project.num_studs, reverse=False)
    for proj in SESSION_1_PROJECTS:
        project_name = proj.proj_name
        project = SESSION.query(Project).filter_by(name=project_name).one()
        session_num = project.session_number
        prefs = SESSION.query(Pref).filter_by(name=project_name)
        prefs = prefs.filter_by(pref_number=4).all()
        student_names = []
        for pref in prefs:
            studs_in_proj = proj.num_studs
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if student.session_1_matched is False:
                if studs_in_proj < MAX_STUDS_PER_GROUP:
                    student_names.append(student.name)
                    student.session_1_matched = True
                    SESSION.add(student)
                    SESSION.commit()
                    if len(proj.students) is 0:
                        proj.students.append(student.name)
                    else:
                        proj.students.append(student.name)

    SESSION_2_PROJECTS.sort(
        key=lambda Project: Project.num_studs, reverse=False)
    for proj in SESSION_2_PROJECTS:
        project_name = proj.proj_name
        project = SESSION.query(Project).filter_by(name=project_name).one()
        session_num = project.session_number
        prefs = SESSION.query(Pref).filter_by(name=project_name)
        prefs = prefs.filter_by(pref_number=4).all()
        student_names = []
        for pref in prefs:
            studs_in_proj = proj.num_studs
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if student.session_2_matched is False:
                if studs_in_proj < MAX_STUDS_PER_GROUP:
                    student_names.append(student.name)
                    student.session_2_matched = True
                    SESSION.add(student)
                    SESSION.commit()
                    if len(proj.students) is 0:
                        proj.students.append(student.name)
                    else:
                        proj.students.append(student.name)

    SESSION_3_PROJECTS.sort(
        key=lambda Project: Project.num_studs, reverse=False)
    for proj in SESSION_3_PROJECTS:
        project_name = proj.proj_name
        project = SESSION.query(Project).filter_by(name=project_name).one()
        session_num = project.session_number
        prefs = SESSION.query(Pref).filter_by(name=project_name)
        prefs = prefs.filter_by(pref_number=4).all()
        student_names = []
        for pref in prefs:
            studs_in_proj = proj.num_studs
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if student.session_3_matched is False:
                if studs_in_proj < MAX_STUDS_PER_GROUP:
                    student_names.append(student.name)
                    student.session_3_matched = True
                    SESSION.add(student)
                    SESSION.commit()
                    if len(proj.students) is 0:
                        proj.students.append(student.name)
                    else:
                        proj.students.append(student.name)

    SESSION_4_PROJECTS.sort(
        key=lambda Project: Project.num_studs, reverse=False)
    for proj in SESSION_4_PROJECTS:
        project_name = proj.proj_name
        project = SESSION.query(Project).filter_by(name=project_name).one()
        session_num = project.session_number
        prefs = SESSION.query(Pref).filter_by(name=project_name)
        prefs = prefs.filter_by(pref_number=4).all()
        student_names = []
        for pref in prefs:
            studs_in_proj = proj.num_studs
            student = SESSION.query(Student).filter_by(
                id=pref.student_id).one()
            if student.session_4_matched is False:
                if studs_in_proj < MAX_STUDS_PER_GROUP:
                    student_names.append(student.name)
                    student.session_4_matched = True
                    SESSION.add(student)
                    SESSION.commit()
                    if len(proj.students) is 0:
                        proj.students.append(student.name)
                    else:
                        proj.students.append(student.name)


def get_unmatched_students():
    """Return students that are unmatched in a project called Not Matched"""
    students = SESSION.query(Student).filter_by(session_1_matched=False).all()
    studs = []
    for student in students:
        studs.append(student.name)
    project_obj = Project_class('Session 1 Not Matched', studs, 0, 0)
    SESSION_1_PROJECTS.append(project_obj)
    students = SESSION.query(Student).filter_by(session_2_matched=False).all()
    studs = []
    for student in students:
        studs.append(student.name)
    project_obj = Project_class('Session 2 Not Matched', studs, 0, 0)
    SESSION_2_PROJECTS.append(project_obj)
    students = SESSION.query(Student).filter_by(session_3_matched=False).all()
    studs = []
    for student in students:
        studs.append(student.name)
    project_obj = Project_class('Session 3 Not Matched', studs, 0, 0)
    SESSION_3_PROJECTS.append(project_obj)
    students = SESSION.query(Student).filter_by(session_4_matched=False).all()
    studs = []
    for student in students:
        studs.append(student.name)
    project_obj = Project_class('Session 4 Not Matched', studs, 0, 0)
    SESSION_4_PROJECTS.append(project_obj)
    return 'it worked'


give_all_prefs()
give_first_prefs()
give_second_prefs()
give_third_prefs()
give_fourth_prefs()
get_unmatched_students()
add_proj_obj_to_database()
print_projects()

#
# if __name__ == '__main__':
#     APP.secret_key = 'super_secret_key'
#     APP.debug = True
#     APP.run(host='0.0.0.0', port=5000)
