import sys
import flask
from flask import Flask, render_template, request
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, engine, Project, Student, Pref
from project_class import Project_class
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

number_of_prefs = 2
max_studs_per_group = 5


def get_raw_score(project):
    project_name = project.name
    prefs = session.query(Pref).filter_by(name=project_name).all()
    return len(prefs)


def get_popularity_score(project):
    project_name = project.name
    prefs = session.query(Pref).filter_by(name=project_name)
    first_prefs = prefs.filter_by(pref_number=1).all()
    second_prefs = prefs.filter_by(pref_number=2).all()
    total_score = len(first_prefs) * 2 + len(second_prefs)
    return total_score


def create_project_object(project):
    project_name = project.name
    session.query(Project).filter_by(name=project_name).one()
    students = []
    raw_score = get_raw_score(project)
    pop_score = get_popularity_score(project)
    proj = Project(project, project_name, students, raw_score, pop_score)
    return proj


def raw_sort():
    projs = []
    projects = session.query(Project).all()
    for proj in projects:
        proj.raw_score = get_raw_score(proj)
        session.add(proj)
        session.commit()
    projects = session.query(Project).all()
    projects.sort(key=lambda Project: Project.raw_score, reverse=False)
    for proj in projects:
        projs.append(proj.name)
    return projs


def pop_sort():
    projs = []
    projects = session.query(Project).all()
    for proj in projects:
        proj.pop_score = get_popularity_score(proj)
        proj.raw_score = get_raw_score(proj)
        session.add(proj)
        session.commit()
    projects = session.query(Project).all()
    projects.sort(key=lambda Project: Project.raw_score, reverse=False)
    for proj in projects:
        if proj.raw_score > 2:
            projs.append(proj.name)
    return projs


def get_underfilled_groups():
    projs = []
    projects = raw_sort()
    for proj in projects:
        project = session.query(Project).filter_by(name=proj).one()
        if project.raw_score < 3:
            projs.append(project.name)
    return projs


def give_all_prefs():
    projs = get_underfilled_groups()
    project_objs = []
    for proj in projs:
        project = session.query(Project).filter_by(name=proj).one()
        students = session.query(Pref).filter_by(name=proj).all()
        student_names = []
        for stud in students:
            student = session.query(Student).filter_by(
                id=stud.student_id).one()
            if student.matched is 0:
                student_names.append(student.first_name)
                student.matched = 1
                session.add(student)
                session.commit()
        raw_score = get_raw_score(project)
        pop_score = get_popularity_score(project)
        project_obj = Project_class(proj, student_names, raw_score, pop_score)
        project_objs.append(project_objs)
        print("project name: " + project_obj.proj_name)
        print("students: ")
        print(project_obj.students)
        print('\n')
    return project_objs


def give_first_prefs():
    projs = pop_sort()
    project_objs = []
    for proj in projs:
        project = session.query(Project).filter_by(name=proj).one()
        students = session.query(Pref).filter_by(name=proj)
        students = students.filter_by(pref_number=1).all()
        student_names = []
        i = 0
        for stud in students:
            student = session.query(Student).filter_by(
                id=stud.student_id).one()
            if student.matched is 0:
                if i < max_studs_per_group:
                    student_names.append(student.first_name)
                    student.matched = 1
                    session.add(student)
                    session.commit()
                    i = i + 1
        raw_score = get_raw_score(project)
        pop_score = get_popularity_score(project)
        project_obj = Project_class(proj, student_names, raw_score, pop_score)
        project_objs.append(project_objs)
        print("project name: " + project_obj.proj_name)
        print("students: ")
        print(project_obj.students)
        print('\n')
    return project_objs


def get_unmatched_students():
    students = session.query(Student).filter_by(matched=0).all()
    studs = []
    for student in students:
        studs.append(student.first_name)
    print("Unmatched Students: ")
    print(studs)
    return studs

give_all_prefs()
give_first_prefs()
get_unmatched_students()
