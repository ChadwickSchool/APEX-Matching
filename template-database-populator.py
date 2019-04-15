project_A = Project(name='A')
project_none = Project(name='Not Matched')

SESSION.add(project_A)
SESSION.commit()

"""Create and add all students to database"""
Bob = Student(first_name='Bob', matched=0)
SESSION.add(Bob)
SESSION.commit()
#instead of just first name you should do firstname_lastname

"""Create and add all prefs to database"""
Bob = SESSION.query(Student).filter_by(first_name='Bob').one()
Bob_first_pref = Pref(pref_number=1, name="A", student_id=1, student=Bob)
Bob_second_pref = Pref(pref_number=2, name="D", student_id=1, student=Bob)
SESSION.add(Bob_first_pref)
SESSION.add(Bob_second_pref)
SESSION.commit()
#you would need to go up to 4 prefs