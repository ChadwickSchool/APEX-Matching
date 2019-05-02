"""Python file of all test cases for algorithm of APEX group making"""
import unittest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from test_database_setup import Project, Base, Student, Pref
from algorithm_16pref import get_raw_score, get_popularity_score
from algorithm_16pref import raw_sort, get_underfilled_groups
from algorithm_16pref import pop_sort, give_all_prefs
from algorithm_16pref import give_first_prefs
from test_application import create_user, get_user_by_email
# from project_class import Project_class

APP = Flask(__name__)
ENGINE = create_engine('sqlite:///testdatabase.db')
Base.metadata.bind = ENGINE
DBSESSION = sessionmaker(bind=ENGINE)
SESSION = DBSESSION()


class BasicTests(unittest.TestCase):
    """Umbrella class of all test cases"""

    # def test_raw_score(self):
    #     """Test if get raw score function works"""
    #     list_score = []
    #     projects = SESSION.query(Project).all()
    #     for proj in projects:
    #         score = get_raw_score(proj)
    #         list_score.append(score)
    #     expected_results = [0]
    #     # print "raw score: "
    #     # print list_score
    #     self.assertEqual(list_score, expected_results)

    # def test_pop_score(self):
    #     """Test if get pop score function works"""
    #     list_score = []
    #     projects = SESSION.query(Project).all()
    #     for proj in projects:
    #         score = get_popularity_score(proj)
    #         list_score.append(score)
    #     expected_results = [0]
    #     # print "pop score: "
    #     # print list_score
    #     self.assertEqual(list_score, expected_results)
    
    def test_max_pop(self):
        """Test to see if any population is above 15"""
        list_num_stud = []
        projects  = SESSION.query(Project).all()
        num_students = 0
        for proj in projects:
            # for students in Project:
            #    num_students += 1
            # num_stud = len(Project.students)
            # if num_students > 15:
            #     list_num_stud.append(num_stud)
            # print proj.students
            num_students = len(proj.students)
        expected_results = []
        # print "Number of students is:"
        # print "student population: "
        # print list_num_stud
        self.assertEqual(list_num_stud, expected_results)
    
    def create_random_project(self):
        SESSION = DBSESSION()
        test = Project(name='That\'s Cringe: Why Fortnite Means the End of Gen Z', session_number = 2)
        SESSION.add(test)
        SESSION.commit()
    
    def test_create_user(self):
        """Test to see if create user works"""
        student_test = Student(name='test', email='test@testycles.com')
        SESSION.add(student_test)
        SESSION.commit()
        is_true = [0]
        students = SESSION.query(Student).all()
        for Student in students:
            student_name = Student.get_user_by_email 
            if student_name == student_test.name:
                print "Student found: "
                print student_name
                is_true += 1
        expected_results = [1]
    #TODO: EVERY STUDENT ASSIGNED
    def all_students_assigned(self):
        unassigned_students = []
        students = SESSION.query(Student).all()
        for Student in students:
            assigned_1 = Student(session_1_matched)
            assigned_2 = Student(session_2_matched)
            assigned_3 = Student(session_3_matched)
            
    #TODO: 80% OF STUDENTS GET FIRST PREF

if __name__ == "__main__":
    unittest.main()
