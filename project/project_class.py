class Project_class:

    def __init__(project, proj_name, students, raw_score, popularity_score):
        '''creates a project with 5 arguments'''
        project.proj_name = proj_name
        project.students = students
        project.raw_score = raw_score
        project.pop_score = popularity_score
        project.num_studs = len(students)


    def __eq__(self, other):
        '''overrides default equals for project class'''
        if isinstance(self, other.__class__):
            return (self.proj_name == other.proj_name
                    and self.students == other.students
                    and self.raw_score == other.raw_score
                    and self.pop_score == other.pop_score)
        return False
