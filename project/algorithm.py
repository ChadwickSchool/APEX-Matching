import sys
import flask
from flask import Flask, render_template, request
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, engine, Project, Student, Pref
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
