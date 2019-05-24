"""Python file of all test cases for algorithm of APEX group making"""
import unittest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from test_database_setup import Project, Base, Student, Pref
from algorithm_16pref import MAX_STUDS_PER_GROUP
# from project_class import Project_class

APP = Flask(__name__)
ENGINE = create_engine('sqlite:///testdatabase.db')
Base.metadata.bind = ENGINE
DBSESSION = sessionmaker(bind=ENGINE)
SESSION = DBSESSION()



class BasicTests(unittest.TestCase):
    """Umbrella class of all test cases"""

    def test_max_pop(self):
        """Test to see if any project's population is above the Maximum Students Per Group limit"""
        list_num_fail = 0
        projects = SESSION.query(Project).all()
        for proj in projects:
            num_students = len(proj.students)
            if num_students >= MAX_STUDS_PER_GROUP:
                list_num_fail += 1
        if list_num_fail > 0:
            print "Number of Overloaded Projects: "
            print list_num_fail
            assert False, "Number of overloaded projects: " + str(list_num_fail)

    def test_all_students_assigned(self):
        """Test to see if all students are ssigned to a project"""
        students = SESSION.query(Student).all()
        for student in students:
            assigned_1 = student.session_1_matched
            assigned_2 = student.session_2_matched
            assigned_3 = student.session_3_matched
            assigned_4 = student.session_4_matched

            if assigned_1 is False:
                assert False
            elif assigned_2 is False:
                assert False
            elif assigned_3 is False:
                assert False
            elif assigned_4 is False:
                assert False
        assert True

    def has_students_been_assigned(self, students, session_num):
        """Checks if all students are assigned"""
        session = DBSESSION()
        projects = session.query(Project).filter_by(session_number=session_num).all()
        are_all_students_matched = True
        for project in projects:
            for student in project.students:
                if student in students:
                    students.remove(student)
                else:
                    are_all_students_matched = False
        return len(students) == 0 and are_all_students_matched

    def test_is_student_in_session(self):
        """Test to see if the student is assigned to the right project"""
        for i in range(1, 5):
            students_list = SESSION.query(Student).all()
            test = self.has_students_been_assigned(students=students_list, session_num=i)
            if test is False:
                assert False
        assert True

    def test_most_students_get_first(self):
        """Tests to see if at least 80% of students students get their first preference"""
        session = DBSESSION()
        numpref = 0
        first_pref = SESSION.query(Pref).filter_by(pref_number=1).all()
        print "Number of first preferences" + str(len(first_pref))
        all_students = SESSION.query(Student).count()
        for pref in first_pref:
            current_student = pref.student
            project = session.query(Project).filter_by(name=pref.name).first()
            if current_student in project.students:
                numpref += 1
        print "Numpref is " + str(numpref)
        thiccpref = float(all_students) * 4
        numpref1 = numpref/thiccpref
        print "Numpref1 is: "
        print numpref1
        if numpref1 <= 0.8:
            assert False

if __name__ == "__main__":
    unittest.main()
