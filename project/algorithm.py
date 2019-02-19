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

def sort_proj_by_size():
    projs = []
    projects = session.query(Project).all()
    projects.sort(key=lambda project: project.size, reverse=False)
    for proj in projects:
        project = [proj.name, proj.size]
        projs.append(project)
    return projs


def get_raw_score(project):
    project_name = project.name
    prefs = session.query(Pref).filter_by(name = project_name).all()
    return len(prefs)


def get_popularity_score(project):
    project_name = project.name
    prefs = session.query(Pref).filter_by(name = project_name)
    first_prefs = prefs.filter_by(pref_number = 1).all()
    second_prefs = prefs.filter_by(pref_number = 2).all()
    total_score = len(first_prefs)*2 + len(second_prefs)
    return total_score
