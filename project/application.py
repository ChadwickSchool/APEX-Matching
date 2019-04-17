import flask
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, send_file
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Student, engine, Project, Pref
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

application = Flask(__name__)
application.wsgi_app = ReverseProxied(application.wsgi_app)
application.config['SECRET_KEY'] = 'super_secret_key'

# CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "APEX Matching Project"

# engine = create_engine('mysql+pymysql://chadwick:godolphins@apex-matching.c0plu8oomro4.us-east-2.rds.amazonaws.com:3306/testdb')
# engine = create_engine('sqlite:///database.db?check_same_thread=false')
engine = create_engine('mysql+pymysql://chadwick:godolphins@apex-matching2.c0plu8oomro4.us-east-2.rds.amazonaws.com:3306/production')
Base.metadata.bind = engine

session_factory = sessionmaker(bind=engine)
DBSession = scoped_session(session_factory)

CHOICES = {
    'choice1': 1,
    'choice2': 2,
    'choice3': 3,
    'choice4': 4
}


@application.route('/', methods=['POST', 'GET'])
def homepage():
    session = DBSession()
    if request.method == 'POST':
        result = request.form
        if not verify_choices(result.items()):
            flash("You must select a project from each session")
        else:
            login_session['chosen_projects'] = result.items()
            return render_template("rank_choices.html", chosen_projects=result.items())
    if 'username' not in login_session:
        return show_login()
    
    user = get_user_by_email(login_session['email'])
    if user is None:
        return show_login()
    preferences = session.query(Pref).filter_by(student_id=user.id).order_by(Pref.pref_number).all()
    
    if user.has_chosen_projects:
        return render_template('student.html', preferences=preferences)
    projects = session.query(Project).all()
    return render_template('homepage.html', projects=projects)


    
@application.route('/rank_choices', methods=['POST'])
def rank_choices():
    choices = request.form.items()
    if verify_choices(choices):
        return create_preferences(choices)
    
    flash("Must have unique choices")
    return render_template("rank_choices.html", chosen_projects=login_session['chosen_projects'])

def verify_choices(choices):
    sessionset = set()
    for choice in choices:
        sessionset.add(choice[1])
    return len(sessionset) == 4

def create_preferences(ranked_projects):
    session = DBSession()
    user = get_user_by_email(login_session['email'])
    user.has_chosen_projects = True
    session.add(user)
    preferences = []
    for choice_num, project_name in sorted(ranked_projects, key=get_key):
        preference = Pref(pref_number=CHOICES[choice_num], name=project_name, student_id=get_user_id(
            login_session['email']))
        session.add(preference)
        preferences.append(preference)
    session.commit()
    flash("Your preferences have been saved")
    return render_template('student.html', preferences=preferences)

def get_key(item):
    return item[0]

@application.route('/database')
def get_database():
    return send_file('./database.db')

@application.route('/show_preferences')
def show_preferences():
    session = DBSession()
    preferences = session.query(Pref).all()
    if preferences is not None:
        user = get_user_by_email(login_session['email'])
        user.has_chosen_projects = True
        session.add(user)
        session.commit()
    return redirect(url_for('homepage'))
    
@application.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@application.route('/gconnect', methods=['POST'])
def gconnect():
    CLIENT_ID = json.loads(
        open('client_secrets.json', 'r').read())['web']['client_id']
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this application.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers[' -Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    # see if user exists, if it doesn't make a new one
    user_id = get_user_id(login_session['email'])
    if user_id is None:
        user_id = create_user(login_session)

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

# User Helper Functions


def create_user(login_session):
    session = DBSession()

    newUser = Student(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(Student).filter_by(email=login_session['email']).one()
    # session.close()
    return user.id


def get_user_by_email(email):
    session = DBSession()
    try:
        user = session.query(Student).filter_by(email=email).one()
        return user
    except:
        return None


def get_user_info(user_id):
    session = DBSession()

    user = session.query(Student).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    session = DBSession()

    try:
        user = session.query(Student).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session
@application.route('/logout')
def disconnect():
    gdisconnect()
    del login_session['gplus_id']
    # Finish cleaning out the login_session
    del login_session['access_token']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    flash("You have been successfully logged out.")
    return redirect(url_for('homepage'))


@application.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    application.secret_key = 'super_secret_key'
    application.debug = True
    # application.run()
    application.run(host='0.0.0.0', port=8000)
