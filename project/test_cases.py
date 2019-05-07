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
from algorithm_16pref import MAX_STUDS_PER_GROUP
from test_application import create_user, get_user_by_email
# from project_class import Project_class

APP = Flask(__name__)
ENGINE = create_engine('sqlite:///testdatabase.db')
Base.metadata.bind = ENGINE
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
        # print "raw score: "
        # print list_score
        self.assertEqual(list_score, expected_results)

    def test_pop_score(self):
        """Test if get pop score function works"""
        list_score = []
        projects = SESSION.query(Project).all()
        for proj in projects:
            score = get_popularity_score(proj)
            list_score.append(score)
        expected_results = [0]
        # print "pop score: "
        # print list_score
        self.assertEqual(list_score, expected_results)
    
    def test_max_pop(self):
        """Test to see if any population is above 15"""
        list_num_stud = 0
        projects  = SESSION.query(Project).all()
        for proj in projects:
            num_students = 0
            num_students = len(proj.students)
            if num_students >= MAX_STUDS_PER_GROUP:
                assert False
    
    def create_random_project(self):
        SESSION = DBSESSION()
        test = Project(name='That\'s Cringe: Why Fortnite Means the End of Gen Z', session_number = 2)
        SESSION.add(test)
        SESSION.commit()
    
    # def test_create_user(self):
    #     """Test to see if create user works"""
    #     student_test = Student(name='test', email='test@testycles.com')
    #     SESSION.add(student_test)
    #     SESSION.commit()
    #     is_true = [0]
    #     students = SESSION.query(Student).all()
    #     for Student in students:
    #         student_name = Student.get_user_by_email 
    #         if student_name == student_test.name:
    #             print "Student found: "
    #             print student_name
    #             is_true += 1
    #     expected_results = [1]
    #TODO: EVERY STUDENT ASSIGNED

    def test_all_students_assigned(self):
        """Test to see if all students are ssigned to a project"""
        students = SESSION.query(Student).all()
        for student in students:
            assigned_1 = student.session_1_matched
            assigned_2 = student.session_2_matched
            assigned_3 = student.session_3_matched
            assigned_4 = student.session_4_matched

            if assigned_1 == False:
                assert False
            elif assigned_2 == False:
                assert False
            elif assigned_3 == False:
                assert False
            elif assigned_4 == False:
                assert False
            else: 
                print "Students Assigned"
    
#TODO: Student is in the session it was assigned to 
    def is_student_in_session(student, session_number):
        """Tests to see if a student is in the session that it is assigned to"""
        #Go through each session and check to see if any session in that session number
        #has that student in it.
        students = SESSION.query(Student).all()
        for student in students:
            #how to get specific session? 
            sess1 = SESSION.query(Project).filter_by(session_number = 1)
            sess2 = SESSION.query(Project).filter_by(session_number = 2)
            sess3 = SESSION.query(Project).filter_by(session_number = 3)
            sess4 = SESSION.query(Project).filter_by(session_number = 4)
            
            for project in sess1:
                has_student = 0
                studentlist = project(students)
                if student in studentlist:
                    has_student += 1
                if has_student1 != 1:
                    assert False
                else:
                    print "Session 1 has student"

            for project in sess2:
                has_student = 0
                studentlist = project(students)
                if student in studentlist:
                    has_student += 1
                if has_student1 != 1:
                    assert False
                else: 
                    print "Session 2 has student"

            for project in sess3:
                has_student = 0
                studentlist = project(students)
                if student in studentlist:
                    has_student += 1
                if has_student1 != 1:
                    assert False
                else:
                    print "Session 3 has student"

            for project in sess4:
                has_student = 0
                studentlist = project(students)
                if student in studentlist:
                    has_student += 1
                if has_student1 != 1:
                    assert False
                else:
                    print "Session 4 has student"


    #TODO: 80% OF STUDENTS GET FIRST PREF
    def most_students_get_first(self):
        students = SESSION.query(Student).all()
        for student in students: 



if __name__ == "__main__":
    unittest.main()
