"""Python file of all test cases for algorithm of APEX group making"""
import unittest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, engine, Project
from algorithm import get_raw_score, get_popularity_score
from algorithm import raw_sort, get_underfilled_groups
from algorithm import pop_sort, give_all_prefs
from algorithm import give_first_prefs
from project_class import Project_class

APP = Flask(__name__)
ENGINE = create_engine('sqlite:///testing.db')
Base.metadata.bind = engine
DBSESSION = sessionmaker(bind=ENGINE)
SESSION = DBSESSION()


class BasicTests(unittest.TestCase):
    """Umbrella class of all test cases"""

    def test_raw_score(self):
        """Test if get raw score function works"""
        list_score = []
        projects = SESSION.query(Project).all()
        for proj in projects:
            score = get_raw_score(proj)
            list_score.append(score)
        expected_results = [0]
        print "raw score: "
        print list_score
        self.assertEqual(list_score, expected_results)

    def test_pop_score(self):
        """Test if get pop score function works"""
        list_score = []
        projects = SESSION.query(Project).all()
        for proj in projects:
            score = get_popularity_score(proj)
            list_score.append(score)
        expected_results = [0]
        print "pop score: "
        print list_score
        self.assertEqual(list_score, expected_results)



if __name__ == "__main__":
    unittest.main()
