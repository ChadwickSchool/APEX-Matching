class Project_class:


    def __init__(project, proj_name, student_name, students):
        '''creates a project with 4 arguments'''
        project.proj_name = proj_name
        project.student_name = student_name
        project.students = students

    def get_size(project):
        return len(project.students)
