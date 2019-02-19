import sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import func

Base = declarative_base()

project_student_link = Table('project_student_link', Base.metadata,
    Column('project_id', Integer, ForeignKey('project.id')),
    Column('student_id', Integer, ForeignKey('student.id')))


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    stud_name = Column(String(32))
    students = relationship('Student', secondary=project_student_link,
                                back_populates='projects')
    @property
    def serialize(self):
        return {
            'id' : self.id,
            'project_name' : self.name,
            'students' : [student.serialize for student in self.students]
        }


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(32))
    last_name = Column(String(32))
    projects = relationship('Project', secondary=project_student_link,
                                back_populates='students')
    @property
    def serialize(self):
        return {
            'id' : self.id,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'projects' : [project.serialize for project in self.projects]
        }


class Pref(Base):
    __tablename__ = 'pref'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pref_number = Column(Integer)
    name = Column(String(32))
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship(Student)

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
