"""Python file of all test cases for algorithm of APEX group making"""
import unittest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Project, Base, Student, Pref
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
#     """Umbrella class of all test cases"""

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
        list_num_fail = 0
        projects  = SESSION.query(Project).all()
        for proj in projects:
            num_students = 0
            num_students = len(proj.students)
            if num_students >= MAX_STUDS_PER_GROUP:
                list_num_fail += 1
        if list_num_fail > 0:
            print "Number of Overloaded Projects: " 
            print list_num_fail
            assert False, "Number of overloaded projects: " + str(list_num_fail)
                
    
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
    def test_is_student_in_session(self):
        """Tests to see if a student is in the session that it is assigned to"""
        #Go through each session and check to see if any session in that session number
        #has that student in it.
        students = SESSION.query(Student).all()
        sess1 = SESSION.query(Project).filter_by(session_number=1).all()
        sess2 = SESSION.query(Project).filter_by(session_number=2).all()
        sess3 = SESSION.query(Project).filter_by(session_number=3).all()
        sess4 = SESSION.query(Project).filter_by(session_number=4).all()
        for student in students:
            #how to get specific session? 
            for project in sess1:
                print "yes"
                has_student = 0
                studentlist = project.students
                if student in studentlist:
                    has_student += 1
                if has_student != 1:
                    assert False
                else:
                    print "Session 1 has student"

            for project in sess2:
                print "yes"
                has_student = 0
                studentlist = project(students)
                if student in studentlist:
                    has_student += 1
                if has_student != 1:
                    assert False
                else: 
                    print "Session 2 has student"

            for project in sess3:
                print "yes"
                has_student = 0
                studentlist = project(students)
                if student in studentlist:
                    has_student += 1
                if has_student != 1:
                    assert False
                else:
                    print "Session 3 has student"

            for project in sess4:
                print "yes"
                has_student = 0
                studentlist = project(students)
                if student in studentlist:
                    has_student += 1
                if has_student != 1:
                    assert False
                else:
                    print "Session 4 has student"
        print "hello world"

    def test_most_students_get_first(self):
        """Tests to see if most students get their first pref"""
        print "this is where the fun begins"
        numpref = 0
        first_pref = SESSION.query(Pref).filter_by(pref_number = 1).all()
        print "asadf"
        all_students = SESSION.query(Student).count()
        print "ill have you know i graduated at the top of my class"
        for pref in first_pref:
            student = pref.student
            projects = SESSION.query(Project).all()
            for project in projects:
                student1 = project.students
                if student not in student1:
                    numpref += 1
        numpref1 = numpref/all_students
        if numpref1 <= 0.8:
            assert False    



if __name__ == "__main__":
    unittest.main()
