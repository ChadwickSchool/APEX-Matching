import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import func

Base = declarative_base()

project_student_link = Table('project_student_link', Base.metadata,
                             Column('project_name', String(500),
                                    ForeignKey('project.name')),
                             Column('student_name', String(500),
                                    ForeignKey('student.name')))


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500))
    stud_name = Column(String(32), nullable=True)
    session_number = Column(Integer, nullable=False)
    raw_score = Column(Integer, nullable=True)
    pop_score = Column(Integer, nullable=True)
    room_number = Column(Integer, nullable=True)
    students = relationship('Student', secondary=project_student_link,
                            backref='projects')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'project_name': self.name,
            'students': [student.serialize for student in self.students]
        }


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    has_chosen_projects = Column(Boolean, default=False)
    picture = Column(String(250))
    session_1_matched = Column(Boolean, default=False)
    session_2_matched = Column(Boolean, default=False)
    session_3_matched = Column(Boolean, default=False)
    session_4_matched = Column(Boolean, default=False)

    @property
    def serialize(self):
        return {
            'name': self.name
        }


class Pref(Base):
    __tablename__ = 'pref'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pref_number = Column(Integer)
    name = Column(String(500))
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship(Student)


engine = create_engine('sqlite:///testing.db')

# engine = create_engine('sqlite:///database.db')

# engine = create_engine('mysql+pymysql://chadwick:godolphins@apex-matching.c0plu8oomro4.us-east-2.rds.amazonaws.com:3306/testdb')

Base.metadata.create_all(engine)
