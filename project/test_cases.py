from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Student, engine, Project, Pref
import os
import unittest
from algorithm import get_raw_score, get_popularity_score
from algorithm import raw_sort, get_underfilled_groups
from algorithm import pop_sort, give_all_prefs
from algorithm import give_first_prefs, get_unmatched_students
from project_class import Project_class

app = Flask(__name__)
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class BasicTests(unittest.TestCase):

    def test_raw_score(self):
        list_score = []
        projects = session.query(Project).all()
        for proj in projects:
            score = get_raw_score(proj)
            list_score.append(score)
        expected_results = [12, 0, 12, 9, 10, 9, 4, 2]
        print(list_score)
        self.assertEqual(list_score, expected_results)

    def test_pop_score(self):
        list_score = []
        projects = session.query(Project).all()
        for proj in projects:
            score = get_popularity_score(proj)
            list_score.append(score)
        expected_results = [18, 0, 18, 12, 15, 14, 7, 3]
        print(list_score)
        self.assertEqual(list_score, expected_results)

    def test_raw_sort(self):
        projs = raw_sort()
        expected_results = ['B', 'H', 'G', 'D', 'F', 'E', 'A', 'C']
        print(projs)
        self.assertEqual(projs, expected_results)

    def test_pop_sort(self):
        projs = pop_sort()
        expected_results = ['G', 'D', 'F', 'E', 'A', 'C']
        print(projs)
        self.assertEqual(projs, expected_results)

    def test_get_underfilled_groups(self):
        projs = get_underfilled_groups()
        expected_results = ['B', 'H']
        self.assertEqual(projs, expected_results)

    def test_give_all_prefs(self):
        projs = give_all_prefs()
        project1 = Project_class('B', [], 0, 0)
        project2 = Project_class('H', ['Tim', 'Liz'], 2, 3)
        projects = [project1, project2]
        return projects == projs

    def test_give_first_prefs(self):
        projs = give_first_prefs()
        project1 = Project_class('G', ['Mary', 'Jen', 'Lin'], 4, 7)
        project2 = Project_class('D', ['Rick', 'Emily', 'Jason'], 9, 12)
        project3 = Project_class('F', ['Rob', 'Mike', 'Pat', 'Steph'], 9, 14)
        project4 = Project_class(
            'E', ['Jon', 'Jerry', 'Barb', 'Ken', 'Laura'], 10, 15)
        project5 = Project_class(
            'A', ['Bob', 'Joe', 'Tom', 'Will', 'Dan'], 12, 18)
        project6 = Project_class(
            'C', ['Jack', 'Jim', 'James', 'Susan', 'Lisa'], 12, 18)
        projects = [project1, project2, project3, project4, project5, project6]
        return projects == projs


if __name__ == "__main__":
    unittest.main()
